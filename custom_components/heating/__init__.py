from homeassistant.helpers.entity import Entity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.const import STATE_UNKNOWN
import aiohttp
import asyncio
from datetime import timedelta
import logging

DOMAIN = "home_assistant_heating"
RESOURCE_URL = "http://your_api_endpoint/data"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    async def async_reload_data(service_call):
        """Service to reload data from the API."""
        coordinator = hass.data[DOMAIN]
        await coordinator.async_request_refresh()

    async def async_send_request(service_call):
        """Service to send a request with new values."""
        coordinator = hass.data[DOMAIN]
        value = service_call.data.get("value")
        await send_request_to_api(value)

    async def send_request_to_api(value):
        """Function to send request with new values to the API."""
        # Replace this with your actual API request logic
        await asyncio.sleep(1)  # Simulate sending request
        print(f"Sending request with value: {value}")

    session = async_get_clientsession(hass)
    coordinator = MyDataUpdateCoordinator(hass, session)

    # Store the coordinator instance in hass.data to access it from services
    hass.data[DOMAIN] = coordinator

    # Register the reload data service
    hass.services.async_register(DOMAIN, "reload_data", async_reload_data)

    # Register the send request service
    hass.services.async_register(DOMAIN, "send_request", async_send_request)

    return True


class MyDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session):
        self.hass = hass
        self.session = session
        self.data = None

        _LOGGER.info('Initiating')

        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),  # adjust as needed
        )
        _LOGGER.info('Initiated')


        

    async def _async_update_data(self):
        try:
            async with self.session.get(RESOURCE_URL) as response:
                self.data = await response.json()

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err


class MySensor(Entity):
    def __init__(self, coordinator):
        self._coordinator = coordinator

    @property
    def name(self):
        return "My Custom Component Sensor"

    @property
    def state(self):
        if self._coordinator.data is None:
            return STATE_UNKNOWN
        return self._coordinator.data.get("value")

    @property
    def extra_state_attributes(self):
        return {"data": self._coordinator.data}

    async def async_update(self):
        await self._coordinator.async_request_refresh()
