from typing import Union, Optional, Iterable
from ipaddress import ip_address, IPv4Address, IPv6Address, IPv4Network, IPv6Network, AddressValueError


Address = Union[IPv4Address, IPv6Address]
Network = Union[IPv4Network, IPv6Network]


def get_real_ip(
	raw_remote_addr: Optional[str],
	raw_forwarded_for: Optional[str],
	*,
	trusted_proxies: Iterable[Network] = tuple(),
) -> Address:
	"""
	Returns IP address of remote host.

	Args:
		raw_remote_addr: Remote IP address of client that sends request.
		raw_forwarded_for: Value of the X-Forwarded-For header.
		trusted_proxies: Networks whose senders are trusted.

	Returns:
		IP address of request sender.

	Raises:
		ValueError (and derivatives) if ip addresses are not valid.
	"""
	if raw_remote_addr is None:
		raise AddressValueError("Remote addr is None")

	remote_addr = ip_address(raw_remote_addr)

	if raw_forwarded_for is None:
		return remote_addr

	for network in trusted_proxies:
		if remote_addr in network:
			return ip_address(raw_forwarded_for)

	return remote_addr
