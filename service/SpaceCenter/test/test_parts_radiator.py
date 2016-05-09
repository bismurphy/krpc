import unittest
import krpctest
import krpc
import time

class TestPartsRadiator(krpctest.TestCase):

    @classmethod
    def setUpClass(cls):
        krpctest.new_save()
        krpctest.launch_vessel_from_vab('PartsRadiator')
        krpctest.remove_other_vessels()
        cls.conn = krpctest.connect(name='TestPartsRadiator')
        cls.vessel = cls.conn.space_center.active_vessel
        cls.parts = cls.vessel.parts
        cls.state = cls.conn.space_center.RadiatorState

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_fixed_radiator(self):
        radiator = next(iter(filter(lambda e: e.part.title == 'Radiator Panel (small)', self.parts.radiators)))
        self.assertFalse(radiator.deployable)
        self.assertTrue(radiator.deployed)
        self.assertEqual(radiator.state, self.state.extended)

    def test_extendable_radiator(self):
        radiator = next(iter(filter(lambda e: e.part.title == 'Thermal Control System (medium)', self.parts.radiators)))
        self.assertTrue(radiator.deployable)
        self.assertFalse(radiator.deployed)
        self.assertEqual(radiator.state, self.state.retracted)

        radiator.deployed = True
        time.sleep(0.1)

        self.assertTrue(radiator.deployed)
        self.assertEqual(radiator.state, self.state.extending)

        while radiator.state == self.state.extending:
            pass
        time.sleep(0.1)

        self.assertTrue(radiator.deployed)
        self.assertEqual(radiator.state, self.state.extended)

        radiator.deployed = False
        time.sleep(0.1)

        self.assertFalse(radiator.deployed)
        self.assertEqual(radiator.state, self.state.retracting)

        while radiator.state == self.state.retracting:
            pass
        time.sleep(0.1)

        self.assertFalse(radiator.deployed)
        self.assertEqual(radiator.state, self.state.retracted)

    def test_break_radiator(self):
        radiator = next(iter(filter(lambda e: e.part.title == 'Thermal Control System (small)', self.parts.radiators)))

        self.assertEqual(radiator.state, self.state.retracted)
        radiator.deployed = True
        while radiator.state == self.state.extending:
            pass
        time.sleep(0.1)

        self.vessel.control.activate_next_stage()
        time.sleep(1)

        self.assertEqual(radiator.state, self.state.broken)

if __name__ == "__main__":
    unittest.main()
