
from datetime import datetime
from zoneinfo import ZoneInfo

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from babel.dates import format_datetime, get_timezone_name

# Shaharlarni aniqlash
geolocator = Nominatim(
    user_agent="RAV_AI_World_Time"
)

tf = TimezoneFinder()

# Til kodlarini Babel formatiga moslash
LANGUAGES = {
    "uz": "uz_UZ",
    "en": "en_US",
    "ru": "ru_RU",
    "fr": "fr_FR",
    "it": "it_IT",
    "de": "de_DE",
    "es": "es_ES",
    "tr": "tr_TR",
    "ar": "ar",
    "zh": "zh_CN",
    "ja": "ja_JP",
    "ko": "ko_KR",
    "pt": "pt_PT",
    "hi": "hi_IN",
    "uk": "uk_UA",
    "pl": "pl_PL",
    "nl": "nl_NL",
    "sv": "sv_SE",
    "fa": "fa_IR",
    "id": "id_ID",
}

def get_world_time(city, language="uz"):

    try:
        # Shaharni topish
        location = geolocator.geocode(
            city,
            timeout=15
        )

        if location is None:
            return "CITY_NOT_FOUND"

        # Vaqt zonasini aniqlash
        timezone_name = tf.timezone_at(
            lng=location.longitude,
            lat=location.latitude
        )

        if timezone_name is None:
            return "TIMEZONE_NOT_FOUND"

        # Shaharning hozirgi vaqtini olish
        city_time = datetime.now(
            ZoneInfo(timezone_name)
        )

        # Javob tilini tanlash
        locale = LANGUAGES.get(
            language.split("-")[0].lower(),
            language
        )

        # Sana va vaqtni tarjima qilish
        date_text = format_datetime(
            city_time,
            "EEEE, d MMMM y",
            locale=locale
        )

        time_text = format_datetime(
            city_time,
            "HH:mm:ss",
            locale=locale
        )

        zone_text = get_timezone_name(
            city_time,
            locale=locale
        )

        return (
            f"Shahar: {location.address}\n"
            f"Sana: {date_text}\n"
            f"Vaqt: {time_text}\n"
            f"Vaqt zonasi: {zone_text}\n"
            f"Time zone ID: {timezone_name}"
        )

    except Exception as error:
        return f"TIME_ERROR: {error}"


# SINOV
if __name__ == "__main__":

    print("RAV AI — WORLD CLOCK")

    city = input("Shahar nomini kiriting: ")
    language = input("Til kodi (uz, en, ru, fr, it): ")

    print(get_world_time(city, language))
