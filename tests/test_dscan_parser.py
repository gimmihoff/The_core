import unittest

from aa_core_hub.services.dscan_parser import parse_dscan


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
                },
                {
                    "name": "Probe",
                    "type_name": "Combat Scanner Probe",
                    "distance": "2 AU",
                },
            ],
        )

    def test_parse_dscan_handles_empty_input(self):
        self.assertEqual(parse_dscan(""), [])
        self.assertEqual(parse_dscan(None), [])
