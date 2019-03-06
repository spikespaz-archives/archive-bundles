import unittest
import requests
import jvman


class AdoptAPIAssetTestCase(unittest.TestCase):
    def test_asset_init(self):
        asset_data_list = requests.get(
            jvman.AdoptAPI.api_base_url + "/latestAssets/releases/openjdk8"
        ).json()

        for asset_data in asset_data_list:
            print(jvman.AdoptAPI.ReleaseAsset(**asset_data).display())


class AdoptAPITestCase(unittest.TestCase):
    def test_search_releases(self):
        for release in jvman.AdoptAPI.search_releases("openjdk8", os="windows"):
            print(release.release_name)

            for asset in release.binaries:
                print(asset.display())
