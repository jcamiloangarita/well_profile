from unittest import TestCase
from well_profile import load
import pandas as pd


class TestLoadTrajectory(TestCase):

    def test_load_from_excel(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well2 = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')

        well.plot(add_well=[well2], names=['well1', 'well2'])

        run_assertions(self, well, 3790)

    def test_inner_pts(self):
        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx',
                    inner_points=1)
        survey_pts = [p for p in well.trajectory if p['pointType'] == 'survey']
        inner_pts = [p for p in well.trajectory if p['pointType'] == 'interpolated']
        self.assertTrue(survey_pts[-1]['md'] > inner_pts[-1]['md'])
        self.assertTrue(survey_pts[-1]['tvd'] > inner_pts[-1]['tvd'])
        self.assertAlmostEqual(max([p['dl'] for p in survey_pts]), max([p['dl'] for p in inner_pts]))
        self.assertAlmostEqual(max([p['dls'] for p in survey_pts]), max([p['dls'] for p in inner_pts]))
        self.assertTrue(any([p['pointType'] == 'interpolated' for p in well.trajectory]))
        self.assertTrue(max([p['inc'] for p in survey_pts]) > max([p['inc'] for p in inner_pts]))

        run_assertions(self, well, 3790)

    def test_load_from_df(self):

        df = pd.read_excel(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/'
                           r'trajectory1.xlsx')
        well = load(df)

        run_assertions(self, well, 3790)

    def test_load_from_dicts(self):

        data = [{'md': 0, 'tvd': 0, 'azimuth': 0, 'inclination': 0},
                {'md': 1, 'tvd': 1, 'azimuth': 0, 'inclination': 0},
                {'md': 2, 'tvd': 2, 'azimuth': 0, 'inclination': 0},
                {'md': 3, 'tvd': 3, 'azimuth': 0, 'inclination': 0},
                {'md': 4, 'tvd': 4, 'azimuth': 0, 'inclination': 0},
                {'md': 5, 'tvd': 5, 'azimuth': 0, 'inclination': 0},
                ]

        well = load(data, points=100)

        run_assertions(self, well, 5)

    def test_load_from_lists(self):

        data = [[0, 1, 2, 3, 4, 5],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 2, 3, 4, 5]]

        well = load(data, points=100)

        run_assertions(self, well, 5)

    def test_load_df(self):

        well = load(load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/'
                         r'trajectory1.xlsx').df())

        run_assertions(self, well, 3790)

    def test_load_initial(self):

        well = load(r'https://github.com/pro-well-plan/well_profile/raw/master/well_profile/tests/trajectory1.xlsx')
        well_initial = well._base_data

        self.assertIsInstance(well, object, msg='main function is not returning an object')
        self.assertIsInstance(well_initial, pd.DataFrame, msg='method is not returning a dataframe')


def run_assertions(obj, well, mdt):
    traj = well.trajectory
    obj.assertIsInstance(well.npoints, int, msg='points is not an integer')
    obj.assertEqual(traj[-1]['md'], mdt, msg='Target depth not reached')
    obj.assertEqual(traj[0]['md'], traj[0]['tvd'], msg='MD and TVD are different at first cell')
    obj.assertIn('pointType', traj[0], msg='pointType property was not found for first trajectory point')
