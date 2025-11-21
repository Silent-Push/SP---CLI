from sp.common.parse_ioc import IOCUtils


def test_parse_public_ipv4():
    dissected_public_ipv4 = IOCUtils("8.8.4.4")
    assert dissected_public_ipv4.valid
    assert dissected_public_ipv4.type == "ipv4"
    assert dissected_public_ipv4.sanitize() == "8.8.4.4"
    assert dissected_public_ipv4.get_result() == "8.8.4.4"
    assert not dissected_public_ipv4.is_md5()
    assert not dissected_public_ipv4.is_64_hash()
    assert not dissected_public_ipv4.is_hash()
    assert dissected_public_ipv4.get_ip_parsed().get("is_global")
    assert not dissected_public_ipv4.get_ip_parsed().get("is_private_ip")
    assert not dissected_public_ipv4.get_ip_parsed().get("is_reserved")
    assert dissected_public_ipv4.get_ip_parsed().get("ip_version") == 4


def test_parse_private_ipv4():
    dissected_private_ipv4 = IOCUtils("10.0.0.1")
    assert dissected_private_ipv4.valid
    assert dissected_private_ipv4.type == "ipv4"
    assert dissected_private_ipv4.sanitize() == "10.0.0.1"
    assert dissected_private_ipv4.get_result() == "10.0.0.1"
    assert not dissected_private_ipv4.is_md5()
    assert not dissected_private_ipv4.is_64_hash()
    assert not dissected_private_ipv4.is_hash()
    assert not dissected_private_ipv4.get_ip_parsed().get("is_global")
    assert dissected_private_ipv4.get_ip_parsed().get("is_private")
    assert not dissected_private_ipv4.get_ip_parsed().get("is_reserved")
    assert dissected_private_ipv4.get_ip_parsed().get("ip_version") == 4


def test_parse_public_ipv6():
    ipv6 = "2345:0425:2CA1:0000:0000:0567:5673:23b5"
    dissected_public_ipv6 = IOCUtils(ipv6)
    assert dissected_public_ipv6.valid
    assert dissected_public_ipv6.type == "ipv6"
    assert dissected_public_ipv6.sanitize() == ipv6
    assert dissected_public_ipv6.get_result() == "2345:425:2ca1::567:5673:23b5"
    assert not dissected_public_ipv6.is_md5()
    assert not dissected_public_ipv6.is_64_hash()
    assert not dissected_public_ipv6.is_hash()
    assert dissected_public_ipv6.get_ip_parsed().get("is_global")
    assert not dissected_public_ipv6.get_ip_parsed().get("is_private_ip")
    assert not dissected_public_ipv6.get_ip_parsed().get("is_reserved")
    assert dissected_public_ipv6.get_ip_parsed().get("ip_version") == 6


def test_parse_private_ipv6():
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    dissected_public_ipv6 = IOCUtils(ipv6)
    assert dissected_public_ipv6.valid
    assert dissected_public_ipv6.type == "ipv6"
    assert dissected_public_ipv6.sanitize() == ipv6
    assert dissected_public_ipv6.get_result() == "2001:db8:85a3::8a2e:370:7334"
    assert not dissected_public_ipv6.is_md5()
    assert not dissected_public_ipv6.is_64_hash()
    assert not dissected_public_ipv6.is_hash()
    assert not dissected_public_ipv6.get_ip_parsed().get("is_global")
    assert dissected_public_ipv6.get_ip_parsed().get("is_private")
    assert not dissected_public_ipv6.get_ip_parsed().get("is_reserved")
    assert dissected_public_ipv6.get_ip_parsed().get("ip_version") == 6


def test_parse_domain():
    dissected_domain = IOCUtils("images.google.com")
    assert dissected_domain.valid
    assert dissected_domain.type == "domain"
    assert dissected_domain.sanitize() == "images.google.com"
    assert dissected_domain.get_result() == "images.google.com"
    assert not dissected_domain.is_md5()
    assert not dissected_domain.is_64_hash()
    assert not dissected_domain.is_hash()
    assert (
            dissected_domain.get_tld_extracted().get("fqdn") == "images.google.com"
    )
    assert dissected_domain.get_tld_extracted().get("subdomain") == "images"
    assert dissected_domain.get_tld_extracted().get("domain") == "google"
    assert dissected_domain.get_tld_extracted().get("suffix") == "com"
    assert dissected_domain.get_ip_parsed() == {}


def test_parse_url():
    url = (
        "http://user:secret@docs.python.org:80/3/library/ElNiño/"
        "urllib.parse.html?highlight=params&x_x=y#url-parsing"
    )
    dissected_url = IOCUtils(url)
    assert dissected_url.valid
    assert dissected_url.type == "url"
    assert dissected_url.sanitize() != url
    assert dissected_url.get_result() == "docs.python.org"
    assert not dissected_url.is_md5()
    assert not dissected_url.is_64_hash()
    assert not dissected_url.is_hash()
    assert dissected_url.get_tld_extracted().get("fqdn") == "docs.python.org"
    assert dissected_url.get_tld_extracted().get("subdomain") == "docs"
    assert dissected_url.get_tld_extracted().get("domain") == "python"
    assert dissected_url.get_tld_extracted().get("suffix") == "org"
    assert dissected_url.get_url_parsed().get("scheme") == "http"
    assert dissected_url.get_url_parsed().get("hostname") == "docs.python.org"
    assert dissected_url.get_url_parsed().get("port") == 80
    assert (
            dissected_url.get_url_parsed().get("path")
            == "/3/library/ElNiño/urllib.parse.html"
    )
    assert dissected_url.get_url_parsed().get("username") == "user"
    assert dissected_url.get_url_parsed().get("password") == "secret"
    assert dissected_url.get_url_parsed().get("fragment") == "url-parsing"
    assert dissected_url.get_ip_parsed() == {}


def test_parse_md5_hash():
    dissected_hash = IOCUtils("8afb4a51c044642a3b523ba6237acaf5")
    assert dissected_hash.valid
    assert dissected_hash.type == "hash"
    assert dissected_hash.sanitize() == "8afb4a51c044642a3b523ba6237acaf5"
    assert dissected_hash.get_result() == "8afb4a51c044642a3b523ba6237acaf5"
    assert dissected_hash.is_md5()
    assert not dissected_hash.is_64_hash()
    assert dissected_hash.is_hash()
    assert dissected_hash.get_ip_parsed() == {}


def test_parse_64_hash():
    dissected_hash = IOCUtils("275451035861481194")
    assert dissected_hash.valid
    assert dissected_hash.type == "hash"
    assert dissected_hash.sanitize() == "275451035861481194"
    assert dissected_hash.get_result() == "275451035861481194"
    assert not dissected_hash.is_md5()
    assert dissected_hash.is_64_hash()
    assert dissected_hash.is_hash()
    assert dissected_hash.get_ip_parsed() == {}


def test_parse_invalid():
    invalid_ioc = IOCUtils(" domain.com")
    assert not invalid_ioc.valid
    assert invalid_ioc.type == "unknown"
    assert invalid_ioc.get_result() == ""
    assert invalid_ioc.get_tld_extracted() == {}
    assert invalid_ioc.get_ip_parsed() == {}
    assert invalid_ioc.get_url_parsed() == {}
