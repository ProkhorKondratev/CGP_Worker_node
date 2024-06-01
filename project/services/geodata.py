from geopandas import GeoDataFrame, GeoSeries
from geoalchemy2.shape import to_shape
from shapely import force_3d
from database import new_session, VectorDataTable, RasterDataTable, ThreeDimDataTable
import os
import aiofiles


class GeoDataHandler:
    @staticmethod
    async def upload_vector(geo_frames: list[GeoDataFrame]):
        async with new_session() as session:
            for frame in geo_frames:
                for idx, row in frame.iterrows():
                    geom = force_3d(row.geometry)
                    attributes = row.drop("geometry").to_dict()
                    data = VectorDataTable(
                        geom=geom.wkt,
                        attributes=attributes,
                    )
                    session.add(data)
            await session.commit()

        return True

    @staticmethod
    async def upload_raster(file_path: str):
        async with new_session() as session:
            raster = RasterDataTable(path=file_path)
            session.add(raster)
            await session.commit()

        return raster.uuid

    @staticmethod
    async def upload_3d_tiles(file_path: str):
        async with new_session() as session:
            threeDimObj = ThreeDimDataTable(path=file_path)
            session.add(threeDimObj)
            await session.commit()

        return threeDimObj.uuid

    @staticmethod
    async def get_vector(uuid: str | None = None):
        if uuid:
            vectors = [await VectorDataTable.get(uuid)]
        else:
            vectors = await VectorDataTable.all()

        geo_frame = GeoDataFrame(
            {
                "id": [str(vector.uuid) for vector in vectors],
                "geometry": [to_shape(vector.geom) for vector in vectors],
                "attributes": [vector.attributes for vector in vectors],
                "crs": "EPSG:4326",
            }
        )

        geo_frame.set_index("id", inplace=True)

        return geo_frame.to_json()

    @staticmethod
    async def get_tiles(uuid: str, z: int, x: int, y: int):
        raster = await RasterDataTable.get(uuid)
        tile_path = os.path.join(raster.path, str(z), str(x), f"{y}.png")

        if not await aiofiles.os.path.exists(tile_path):
            raise FileNotFoundError

        return tile_path

    @staticmethod
    async def get_3d_tiles(uuid: str, path: str):
        raster = await ThreeDimDataTable.get(uuid)
        tile_path = os.path.join(raster.path, path)

        if not await aiofiles.os.path.exists(tile_path):
            raise FileNotFoundError

        return tile_path
