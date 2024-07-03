# Solved import resolution issues by using a virtual environment, and importing the
# modules as modules of the myHealth package.
# Solution provided by https://py-pkgs.org/05-testing.html#test-structure.
from myHealth.medication import *
import myHealth.utility as utility
import unittest
from unittest.mock import *

class mock_entries:
    """Encapsulates sample entries used for testing."""
    VALID_LEVOTHYROXINE = {
        "name": "levothyroxine",
        "purpose": "hypothyroidism",
        "dose": 75.0,
        "units": "mcg",
        "times": {
            'BB': 1,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 0,
            },
    }
    VALID_LEVOTHYROXINE_CSV = {
        "name": "levothyroxine",
        "purpose": "hypothyroidism",
        "dose": 75.0,
        "units": "mcg",
        "times": "{'BB': 1, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 0,}",
    }
    mock_valid_levothyroxine = Mock(**VALID_LEVOTHYROXINE)
    mock_valid_levothyroxine.configure_mock(name=VALID_LEVOTHYROXINE["name"])

    VALID_EDITED_LEVOTHYROXINE = {
        "name": "levothyroxine",
        "purpose": "painkiller",
        "dose": 500,
        "units": "mg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
            },
    }
    VALID_EDITED_LEVOTHYROXINE_CSV = {
        "name": "levothyroxine",
        "purpose": "painkiller",
        "dose": 500,
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    mock_valid_edited_levothyroxine = Mock(**VALID_EDITED_LEVOTHYROXINE)
    mock_valid_edited_levothyroxine.configure_mock(name=VALID_EDITED_LEVOTHYROXINE["name"])

    VALID_FRUSEMIDE = {
        "name": "frusemide",
        "purpose": "edema",
        "dose": 40.0,
        "units": "mg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
        },
    }
    VALID_FRUSEMIDE_CSV = {
        "name": "frusemide",
        "purpose": "edema",
        "dose": 40.0,
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    mock_valid_frusemide = Mock(**VALID_FRUSEMIDE)
    mock_valid_frusemide.configure_mock(name=VALID_FRUSEMIDE["name"])

    VALID_INSULIN = {
        "name": "insulin novamix 30",
        "purpose": "hyperglycemia",
        "dose": 18.0,
        "units": "units",
        "times": {
            'BB': 1,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 1,
            'AD': 0,
            'AAWN': 0,
        },
    }
    VALID_INSULIN_CSV = {
        "name": "insulin novamix 30",
        "purpose": "hyperglycemia",
        "dose": 18.0,
        "units": "units",
        "times": "{'BB': 1, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 1, 'AD': 0, 'AAWN': 0,}",
    }
    mock_valid_insulin = Mock(**VALID_INSULIN)
    mock_valid_insulin.configure_mock(name=VALID_INSULIN["name"])

    VALID_GLYPRIN = {
        "name": "glyprin",
        "purpose": None,
        "dose": 0.0,
        "units": None,
        "times": {
            'BB': 0,
            'AB': 1,
            'BL': 0,
            'AL': 0,
            'BD': 1,
            'AD': 0,
            'AAWN': 0,
        },
    }
    VALID_GLYPRIN_CSV = {
        "name": "glyprin",
        "purpose": "",
        "dose": 0.0,
        "units": "",
        "times": "{'BB': 0, 'AB': 1, 'BL': 0, 'AL': 0, 'BD': 1, 'AD': 0, 'AAWN': 0,}",
    }
    mock_valid_glyprin = Mock(**VALID_GLYPRIN)
    mock_valid_glyprin.configure_mock(name=VALID_GLYPRIN["name"])

    VALID_PANADOL = {
        "name": "panadol",
        "purpose": "painkiller",
        "dose": 500,
        "units": "mg",
        "times": {
            "BB": 0,
            "AB": 0,
            "BL": 0,
            "AL": 0,
            "BD": 0,
            "AD": 0,
            "AAWN": 1,
        },
    }
    VALID_PANADOL_CSV = {
        "name": "panadol",
        "purpose": "painkiller",
        "dose": 500,
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    mock_valid_panadol = Mock(**VALID_PANADOL)
    mock_valid_panadol.configure_mock(name=VALID_PANADOL["name"])

    mock_valid_medlist = [mock_valid_levothyroxine, mock_valid_frusemide, mock_valid_insulin, mock_valid_glyprin]
    #mock_valid_edited_medlist = [mock_valid_edited_levothyroxine, mock_valid_frusemide, mock_valid_insulin, mock_valid_glyprin]
    VALID_DICTS = [VALID_LEVOTHYROXINE, VALID_FRUSEMIDE, VALID_INSULIN, VALID_GLYPRIN]
    VALID_CSV = [VALID_LEVOTHYROXINE_CSV, VALID_FRUSEMIDE_CSV, VALID_INSULIN_CSV, VALID_GLYPRIN_CSV]
    
    INVALID_EMPTY_NAME = {
        "name": "",
        "purpose": "cure all",
        "dose": 1.0,
        "units": "mg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
            },
    }
    INVALID_EMPTY_NAME_CSV = {
        "name": "",
        "purpose": "cure all",
        "dose": 1.0,
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    INVALID_NONASCII_PURPOSE = {
        "name": "panacea",
        "purpose": "curé àll",
        "dose": 1.0,
        "units": "mg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
            },
    }
    INVALID_NONASCII_PURPOSE_CSV = {
        "name": "panacea",
        "purpose": "curé àll",
        "dose": 1.0,
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    INVALID_NONFLOAT_DOSE = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": "cat",
        "units": "mg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
            },
    }
    INVALID_NONFLOAT_DOSE_CSV = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": "cat",
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    INVALID_NEGATIVE_DOSE = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": -10,
        "units": "mg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
            },
    }
    INVALID_NEGATIVE_DOSE_CSV = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": -10,
        "units": "mg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    INVALID_UNITS = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": 10,
        "units": "kg",
        "times": {
            'BB': 0,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 1,
            },
    }
    INVALID_UNITS_CSV = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": 10,
        "units": "kg",
        "times": "{'BB': 0, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 1,}",
    }
    INVALID_NEGATIVE_TIMES = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": 10,
        "units": "g",
        "times": {
            'BB': -1,
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 0,
            },
    }
    INVALID_NEGATIVE_TIMES_CSV = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": 10,
        "units": "g",
        "times": "{'BB': -1, 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 0,}",
    }
    INVALID_NONINT_TIMES = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": 10,
        "units": "g",
        "times": {
            'BB': "infinity",
            'AB': 0,
            'BL': 0,
            'AL': 0,
            'BD': 0,
            'AD': 0,
            'AAWN': 0,
            },
    }
    INVALID_NONINT_TIMES_CSV = {
        "name": "panacea",
        "purpose": "cure all",
        "dose": 10,
        "units": "g",
        "times": "{'BB': 'infinity', 'AB': 0, 'BL': 0, 'AL': 0, 'BD': 0, 'AD': 0, 'AAWN': 0,}",
    }


class test_add_medication(unittest.TestCase):
    @patch("myHealth.medication.Medicine", autospec=True)
    # Issues with "target" fixed: add_medication will look up Medicine in medication, not locally. Only initial references can be localised.
    def test_add_valid(self, mock_Medicine):
        
        mock_Medicine.create.return_value = mock_entries.mock_valid_panadol
        new_mock_valid_medlist, message = add_medication(mock_entries.mock_valid_medlist)  # Unittest does not allow self-assignment.
        
        mock_Medicine.create.assert_called_once_with()
        self.assertIn(mock_entries.mock_valid_panadol, new_mock_valid_medlist)
        self.assertEqual(message, f"{mock_entries.mock_valid_panadol.name.title()} successfully added. Returning to myMedication...")
    
    @patch("myHealth.medication.Medicine", autospec=True)
    def test_keyboard_interrupt(self, mock_Medicine):
        
        mock_Medicine.create.side_effect = KeyboardInterrupt
        new_mock_valid_medlist, message = add_medication(mock_entries.mock_valid_medlist)
        
        mock_Medicine.create.assert_called_once_with()
        self.assertNotIn(mock_entries.mock_valid_panadol, new_mock_valid_medlist)
        self.assertListEqual(mock_entries.mock_valid_medlist, new_mock_valid_medlist)
        self.assertEqual(message, "\nAction disrupted. No changes will be made. Returning to myMedication...")


class test_edit_medication(unittest.TestCase):
    # Setter will not be tested here, as it'll be tested under test_select_medication.
    # Numbers left as int/float because setter cannot be activated. No data validation here as we're dealing with mocks.
    # Unable to change name without calling constructor or configure_mock.
    @patch("builtins.input", side_effect=["painkiller", 500, "mg", "aa", " bb ", 2, "aawn", 1, "", "void", ""])
    @patch.object(utility, "display")
    @patch.object(utility, "yes_or_no", side_effect=[False, True, True, True])
    # Need to provide the return values for all calls, otherwise StopIteration will be raised by next.
    @patch.object(Medicine, "get_non_empty_string", return_value="levothyroxine")
    def test_successful_edit(self, mock_gnes, mock_yn, mock_display, mock_input):
        updated_list, message = edit_medication(mock_entries.mock_valid_medlist)
        
        self.assertEqual(mock_input.call_count, 11)
        self.assertEqual(mock_yn.call_count, 4)
        mock_gnes.assert_called_once()
        
        # Note that IDs are compared. Copies of mocks will retain the ID of the original, and editing will not change a mock's ID.
        self.assertListEqual(
            updated_list,
            mock_entries.mock_valid_medlist
        )
        self.assertEqual(len(updated_list), 4)
        
        for med in mock_entries.mock_valid_medlist:
            self.assertIn(med, updated_list)
            
        self.assertEqual(
            message,
            "Returning to myMedication..."
        )
    
    @patch.object(Medicine, "get_non_empty_string", return_value="non-existent")
    def test_failed_edit(self, mock_gnes):
        with self.assertRaises(KeyError):
            remove_medication(mock_entries.mock_valid_medlist)
        
        mock_gnes.assert_called_once()
    
    @patch.object(Medicine, "get_non_empty_string", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_gnes):
        updated_list, message = edit_medication(mock_entries.mock_valid_medlist)
        
        mock_gnes.assert_called_once()
        self.assertListEqual(
            updated_list,
            mock_entries.mock_valid_medlist
        )
        self.assertEqual(len(updated_list), 4)
        
        for med in mock_entries.mock_valid_medlist:
            self.assertIn(med, updated_list)
            
        self.assertEqual(
            message,
            "\nAction disrupted. No changes will be made. Returning to myMedication..."
        )


class test_remove_medication(unittest.TestCase):
    @patch.object(utility, "yes_or_no", return_value=True)
    @patch.object(Medicine, "get_non_empty_string", return_value="frusemide")
    def test_successful_removal(self, mock_gnes, mock_yn):
        updated_list, message = remove_medication(mock_entries.mock_valid_medlist)
        
        mock_gnes.assert_called_once()
        mock_yn.assert_called_once()
        self.assertListEqual(
            updated_list,
            [mock_entries.mock_valid_levothyroxine, mock_entries.mock_valid_insulin, mock_entries.mock_valid_glyprin]
        )
        self.assertEqual(len(updated_list), 3)
        self.assertNotIn(mock_entries.mock_valid_frusemide, updated_list)
        self.assertEqual(
            message,
            f"The entry for {mock_entries.mock_valid_frusemide.name.title()} has been deleted successfully. Returning to myMedication..."
        )
    
    @patch.object(utility, "yes_or_no", return_value=False)  # "If "n" is returned, it'll be interpreted as True!
    @patch.object(Medicine, "get_non_empty_string", return_value="frusemide")
    def test_successful_cancellation(self, mock_gnes, mock_yn):
        updated_list, message = remove_medication(mock_entries.mock_valid_medlist)
        
        mock_gnes.assert_called_once()
        mock_yn.assert_called_once()
        #self.assertListEqual(updated_list, mock_entries.mock_valid_medlist)
        self.assertEqual(len(updated_list), 4)
        self.assertIn(mock_entries.mock_valid_frusemide, updated_list)
        self.assertEqual(
            message,
            f"The entry for {mock_entries.mock_valid_frusemide.name.title()} will not be deleted. Returning to myMedication..."
        )
        
    @patch.object(Medicine, "get_non_empty_string", return_value="non-existent")
    def test_failed_removal(self, mock_gnes):
        with self.assertRaises(KeyError):
            remove_medication(mock_entries.mock_valid_medlist)
        
        mock_gnes.assert_called_once()
    
    @patch.object(Medicine, "get_non_empty_string", side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt(self, mock_gnes):
        updated_list, message = remove_medication(mock_entries.mock_valid_medlist)
        
        mock_gnes.assert_called_once()
        self.assertListEqual(
            updated_list,
            mock_entries.mock_valid_medlist
        )
        self.assertEqual(len(updated_list), 4)
        
        for med in mock_entries.mock_valid_medlist:
            self.assertIn(med, updated_list)
            
        self.assertEqual(
            message,
            "\nAction disrupted. No changes will be made. Returning to myMedication..."
        )


class test_select_medication(unittest.TestCase):
    def test_select_name(self):
        results = select_medication("name", "frusemide", mock_entries.mock_valid_medlist)
        self.assertListEqual(results, [1])
        
        with self.assertRaises(KeyError):
            select_medication("name", "panacea", mock_entries.mock_valid_medlist)
    
    def test_select_purpose(self):
        results = select_medication("purpose", "hyperglycemia", mock_entries.mock_valid_medlist)
        self.assertListEqual(results, [2])
        
        with self.assertRaises(KeyError):
            select_medication("purpose", "constipation", mock_entries.mock_valid_medlist)
    
    def test_select_times(self):
        results = select_medication("times", "BB", mock_entries.mock_valid_medlist)
        self.assertListEqual(results, [0, 2])
        
        with self.assertRaises(KeyError):
            select_medication("times", "BL", mock_entries.mock_valid_medlist)


class test_load_medication(unittest.TestCase):
    @patch("builtins.open", autospec=True)  # Found with import builtins; dir(builtins)
    def test_invalid_file(self, mock_open):
        mock_open.side_effect = OSError
        with self.assertRaises(OSError):
            load_medication()
            mock_open.assert_called_once_with("myMedication.csv", newline="")
    
    @patch("builtins.open", autospec=True)
    @patch("csv.DictReader", autospec=True)  # Decorators are applied bottom-up.
    def test_valid_database(self, mock_DictReader, mock_open):  # Proxy for testing Medicine.__init__ and the setters.
        
        mock_DictReader.return_value = mock_entries.VALID_CSV
        med_data, message = load_medication()
        
        self.assertEqual(len(med_data), 4)
        for med in med_data:
            self.assertIsInstance(med, Medicine)
        for i in range(len(med_data)):
            self.assertEqual(med_data[i].name, mock_entries.VALID_DICTS[i]["name"])
            self.assertEqual(med_data[i].purpose, mock_entries.VALID_DICTS[i]["purpose"])
            self.assertEqual(med_data[i].dose, mock_entries.VALID_DICTS[i]["dose"])
            self.assertEqual(med_data[i].units, mock_entries.VALID_DICTS[i]["units"])
            self.assertEqual(med_data[i].times, mock_entries.VALID_DICTS[i]["times"])
            
        self.assertEqual(message, "Medications loaded successfully.")

    @patch("builtins.open", autospec=True)
    @patch("csv.DictReader", autospec=True)
    def test_invalid_database(self, mock_DictReader, mock_open):  # Proxy for testing Medicine.__init__ and the setters.
        
        mock_DictReader.return_value = [mock_entries.INVALID_EMPTY_NAME_CSV]
        with self.assertRaises(ValueError):
            load_medication()
        
        mock_DictReader.return_value = [mock_entries.INVALID_NONASCII_PURPOSE_CSV]
        with self.assertRaises(ValueError):
            load_medication()
        
        mock_DictReader.return_value = [mock_entries.INVALID_NONFLOAT_DOSE_CSV]
        with self.assertRaises(ValueError):
            load_medication()
            
        mock_DictReader.return_value = [mock_entries.INVALID_NEGATIVE_DOSE_CSV]
        with self.assertRaises(ValueError):
            load_medication()
        
        mock_DictReader.return_value = [mock_entries.INVALID_UNITS_CSV]
        with self.assertRaises(ValueError):
            load_medication()
        
        mock_DictReader.return_value = [mock_entries.INVALID_NEGATIVE_TIMES_CSV]
        with self.assertRaises(ValueError):
            load_medication()
        
        mock_DictReader.return_value = [mock_entries.INVALID_NONINT_TIMES_CSV]
        with self.assertRaises(ValueError):
            load_medication()


class test_query(unittest.TestCase):
    @patch("myHealth.medication.utility")  # Local reference to the module created in medication.
    @patch.object(Medicine, "get_non_empty_string", side_effect=["non_existent", "", "name", "felodipine"])
    def test_query_name(self, mock_gnes, mock_utility):  # MagicMock created must be passed as argument into the decorated function.
        results = query()
        self.assertEqual(mock_gnes.call_count, 4)  # Remember that non-empty strings will be accepted here.
        self.assertTupleEqual(results, ("name", "felodipine"))
    
    @patch("myHealth.medication.utility")
    @patch.object(Medicine, "get_non_empty_string", side_effect=["purpose", "hypertension"])
    def test_query_purpose(self, mock_gnes, mock_utility):
        results = query()
        self.assertEqual(mock_gnes.call_count, 2)
        self.assertTupleEqual(results, ("purpose", "hypertension"))
    
    @patch("myHealth.medication.utility")
    @patch("builtins.input", side_effect=["AA", "bb"])
    @patch.object(Medicine, "get_non_empty_string", return_value="times")
    def test_query_times(self, mock_gnes, mock_input, mock_utility):
        results = query()
        self.assertEqual(mock_gnes.call_count, 1)
        self.assertEqual(mock_input.call_count, 2)
        self.assertTupleEqual(results, ("times", "BB"))


if __name__ == "__main__":
    unittest.main()