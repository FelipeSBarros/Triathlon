from pathlib import Path
import fiona
import geopandas as gpd
import movingpandas as mpd
import logging
from datetime import datetime
import pandas as pd
GPX_PATH = Path("./gpx-files")
TRACK_LAYER = "track_points"


def save_track(track_gdf, gpkg_path="./data", gpkg_name="Triathlon.gpkg", name=None):
    gpkg_path = Path(gpkg_path)
    full_path = gpkg_path.joinpath(gpkg_name)
    if not gpkg_path.exists():
        gpkg_path.mkdir()
    track_gdf.to_file(
        full_path,
        layer=name,
        driver="GPKG",
    )
    logging.warning(f"file {name} saved on {full_path}")


def gpx_2_gpkg(
    gpx_path=GPX_PATH,
    layer="track_points",
):
    gpx_file_list = [file for file in gpx_path.glob("*.gpx")]
    for file in gpx_file_list:
        # file = gpx_file_list[-5]
        track_name = file.name.split('.')[0]
        gpx_original = fiona.open(file, layer=layer)
        # convert to geodataframe
        track_gdf = gpd.GeoDataFrame.from_features(
            [feature for feature in gpx_original], crs=gpx_original.crs
        )
        save_track(
            track_gdf,
            name=f"{track_name}_track_points",
        )

        # conversion to a movingpandas' track
        logging.info(f"Creating trajectory from track points")
        if not "time" in track_gdf.columns:
            logging.warning(f"{track_name} has no datetime information. Creatign a fake one")
            track_gdf['time'] = pd.to_timedelta(track_gdf.index * 60, unit='S') + datetime(2000,1,1, 0, 0)
            # track_gdf.info()
            # pd.to_datetime(track_gdf['time'])

        trajectory = mpd.Trajectory(
            df=track_gdf, traj_id="track_seg_point_id", t="time"
        )
        # calculate few track attributes
        trajectory.add_acceleration(overwrite=True)
        trajectory.add_distance(overwrite=True)  # in meters
        trajectory.add_speed(overwrite=True)  # in meters per second
        trajectory.add_timedelta(overwrite=True)
        trajectory.df.timedelta = trajectory.df.timedelta.dt.total_seconds()
        trajectory = trajectory.to_line_gdf()
        trajectory.crs = track_gdf.crs
        save_track(
            track_gdf=trajectory,
            name=f"{file.name.split('.')[0]}_trajectory",
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Converting GPX to GPKG")
    gpx_2_gpkg()
    logging.info("Convertion finished")
