from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from services import user_preferences


class UserPreferencesTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_database_path = user_preferences.DATABASE_PATH
        user_preferences.DATABASE_PATH = Path(self.temp_dir.name) / "test.sqlite3"
        await user_preferences.initialize_preferences()

    async def asyncTearDown(self) -> None:
        user_preferences.DATABASE_PATH = self.original_database_path
        self.temp_dir.cleanup()

    async def test_referral_is_counted_once(self) -> None:
        created, credited = await user_preferences.register_user(1001)
        self.assertTrue(created)
        self.assertFalse(credited)

        created, credited = await user_preferences.register_user(2002, 1001)
        self.assertTrue(created)
        self.assertTrue(credited)

        created, credited = await user_preferences.register_user(2002, 1001)
        self.assertFalse(created)
        self.assertFalse(credited)

        settings = await user_preferences.get_settings(1001)
        self.assertEqual(settings["referral_count"], 1)

    async def test_self_referral_is_not_counted(self) -> None:
        await user_preferences.register_user(3003)
        created, credited = await user_preferences.register_user(3003, 3003)

        self.assertFalse(created)
        self.assertFalse(credited)
        settings = await user_preferences.get_settings(3003)
        self.assertEqual(settings["referral_count"], 0)

    async def test_unknown_referrer_is_not_credited(self) -> None:
        created, credited = await user_preferences.register_user(4004, 9999)

        self.assertTrue(created)
        self.assertFalse(credited)
        settings = await user_preferences.get_settings(9999)
        self.assertEqual(settings["referral_count"], 0)

    async def test_language_and_notification_preferences_persist(self) -> None:
        await user_preferences.register_user(5005)
        await user_preferences.set_language(5005, "ru")

        notifications_enabled = await user_preferences.toggle_notifications(5005)
        self.assertFalse(notifications_enabled)

        settings = await user_preferences.get_settings(5005)
        self.assertEqual(settings["language"], "ru")
        self.assertFalse(settings["notifications_enabled"])


if __name__ == "__main__":
    unittest.main()
