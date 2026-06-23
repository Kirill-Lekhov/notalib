from notalib.ipaddress import get_real_ip

from ipaddress import AddressValueError, IPv4Network, IPv4Address, IPv6Network, IPv6Address

import pytest


class TestGetRealIP:
	def test_normal_v4(self):
		assert get_real_ip("127.0.0.1", None) == IPv4Address("127.0.0.1")
		assert get_real_ip("127.0.0.1", "192.168.0.1") == IPv4Address("127.0.0.1")
		ip = get_real_ip("127.0.0.1", "192.168.0.1", trusted_proxies=(IPv4Network("192.168.0.1"), ))
		assert ip == IPv4Address("127.0.0.1")
		ip = get_real_ip("127.0.0.1", "192.168.0.1", trusted_proxies=(IPv4Network("127.0.0.1"), ))
		assert ip == IPv4Address("192.168.0.1")

	def test_normal_v6(self):
		assert get_real_ip("::1", None) == IPv6Address("::1")
		assert get_real_ip("::1", "fd00::1") == IPv6Address("::1")
		ip = get_real_ip("::1", "fd00::1", trusted_proxies=(IPv6Network("fd00::1"), ))
		assert ip == IPv6Address("::1")
		ip = get_real_ip("::1", "fd00::1", trusted_proxies=(IPv6Network("::1"), ))
		assert ip == IPv6Address("fd00::1")

	def test_error(self):
		with pytest.raises(AddressValueError, match="Remote addr is None"):
			get_real_ip(None, None)

		with pytest.raises(ValueError):
			get_real_ip("hello world", None)

		with pytest.raises(ValueError):
			get_real_ip("127.0.0.1", "hello world", trusted_proxies=(IPv4Network("127.0.0.1"), ))
