import logging
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.const import (CONF_NAME, CONF_PREFIX, CONF_ICON, CONF_SCAN_INTERVAL, CONF_UNIT_OF_MEASUREMENT)
from datetime import timedelta
import voluptuous as vol
from json import loads
import requests

_LOGGER = logging.getLogger(__name__)

DEFAULT_ICON = 'mdi:package-variant-closed'
DEFAULT_UNIT_OF_MEASUREMENT = '원'
DEFAULT_SCAN_INTERVAL = timedelta(hours=2)
SCAN_INTERVAL = DEFAULT_SCAN_INTERVAL
DEFAULT_PREFIX = 'Coupang'

URL_BASE = 'https://m.coupang.com/vm/v4/enhanced-pdp/products/'
REQUEST_HEADER = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}

_ITEM_SCHEMA = vol.All(
    vol.Schema({
        vol.Required('product_id'): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.icon
    })
)

_ITEMS_SCHEMA = vol.Schema([_ITEM_SCHEMA])

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required('items'): _ITEMS_SCHEMA,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_PREFIX, default=DEFAULT_PREFIX): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Initiate coupang_price sensor"""
    items = config.get('items')
    SCAN_INTERVAL = config.get(CONF_SCAN_INTERVAL)
    unit_of_measurement = config.get(CONF_UNIT_OF_MEASUREMENT)
    prefix = config.get(CONF_PREFIX).strip()
    sensors = []

    for item in items:
        try:
            sensors.append(CoupangPriceSensor(item, unit_of_measurement, prefix))
        except ValueError as e:
            _LOGGER.error(e)

    add_devices(sensors, True)

class CoupangPriceSensor(Entity):
    def __init__(self, item, unit_of_measurement, prefix):
        """initial values"""
        self._product_id = item.get('product_id')
        self._name = item.get(CONF_NAME)
        self._icon = item.get(CONF_ICON)
        self._unit_of_measurement = unit_of_measurement
        self._prefix = prefix
        self._info = {}
    
    @property
    def name(self):
        """Return the name of the sensor."""
        if not self._name:
            if not self._info['product_name']:
                self._name = 'Unknown Item'
            else:
               self._name = self._info['product_name']
        return self._prefix + ' ' + self._name

    @property
    def icon(self):
        """Return the icon for the frontend."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return unit of measurement"""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the sale price of the item."""
        return self._info['price']
        
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._info
    
    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Update sensor value"""
        url = URL_BASE + self._product_id
        r = requests.get(url, headers=REQUEST_HEADER, timeout=5)
        if r.status_code!=200:
            _LOGGER.error('HTTP request failed: ' + url)
        
        try:
            j = loads(r.text)
            info = j['rData']['vendorItemDetail']['item']
            """Parse useful info"""
            self._info['product_id'] = self._product_id
            self._info['price'] = info['salesPrice']
            self._info['sold_out'] = info['soldOut']
            self._info['vendor'] = info['vendor']['name']
            self._info['product_name'] = info['productName']
            self._info['delivery_type'] = info['deliveryType']
            if 'unitPrice' in info:
                self._info['unit_price'] = info['unitPrice']
            
        except Exception as e:
            _LOGGER.error(e)