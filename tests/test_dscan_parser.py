import unittest

from aa_core_hub.services.dscan_parser import classify_dscan_type, parse_dscan


class DScanParserTests(unittest.TestCase):
    def test_parse_dscan_extracts_tab_delimited_rows(self):
        text = (
            "Astrahus\tUpwell Structure\t1,000 km\n"
            "\n"
            "Invalid row without tabs\n"
            "Probe\tCombat Scanner Probe\t2 AU"
        )

        self.assertEqual(
            parse_dscan(text),
            [
                {
                    "name": "Astrahus",
                    "type_name": "Upwell Structure",
                    "distance": "1,000 km",
                    "category": "STRUCTURE",
                },
                {
                    "name": "Probe",
                    "type_name": "Combat Scanner Probe",
                    "distance": "2 AU",
                    "category": "PROBE",
                },
            ],
        )

    def test_parse_dscan_handles_empty_input(self):
        self.assertEqual(parse_dscan(""), [])
        self.assertEqual(parse_dscan(None), [])

    def test_parse_dscan_extracts_id_name_type_distance_rows(self):
        self.assertEqual(
            parse_dscan("11190\tHostile Pilot\tSentinel\t117 km"),
            [
                {
                    "name": "Hostile Pilot",
                    "type_name": "Sentinel",
                    "distance": "117 km",
                    "category": "SHIP_OR_OBJECT",
                },
            ],
        )

    def test_parse_dscan_uses_id_as_name_when_object_name_is_blank(self):
        self.assertEqual(
            parse_dscan("1035466617946\t\tUpwell Structure\t1,000 km"),
            [
                {
                    "name": "1035466617946",
                    "type_name": "Upwell Structure",
                    "distance": "1,000 km",
                    "category": "STRUCTURE",
                },
            ],
        )

    def test_classify_dscan_type_identifies_core_categories(self):
        self.assertEqual(classify_dscan_type("Astrahus"), "STRUCTURE")
        self.assertEqual(classify_dscan_type("Upwell Structure"), "STRUCTURE")
        self.assertEqual(classify_dscan_type("Ansiblex Jump Gate"), "SOV")
        self.assertEqual(classify_dscan_type("Stargate"), "SOV")
        self.assertEqual(classify_dscan_type("Combat Scanner Probe"), "PROBE")
        self.assertEqual(classify_dscan_type(""), "")
