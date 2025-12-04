import os

from dotenv import load_dotenv

load_dotenv()

CRLF = "\r\n"
"""The prompt line break"""
API_URL = os.environ.get("SILENT_PUSH_API_URL", "https://app.silentpush.com/api/")
"""The Silent Push API URL, you can export it to your prompt if needs to change or use .env"""
API_KEY = os.environ.get("SILENT_PUSH_API_KEY")
"""Your Silent Push API key"""

if API_URL is None:
    raise EnvironmentError(
        "Please set the Silent Push API URL in your environment.\n"
        '\texport SILENT_PUSH_API_URL="'
        'https://app.silentpush.com/api/"'
    )

if API_KEY is None:
    raise EnvironmentError(
        "Please set your Silent Push API key in your environment.\n"
        '\texport SILENT_PUSH_API_KEY="YOUR-API-KEY"'
    )


def get_initial_commands() -> set:
    """
    The available commands to the app, any new created command needs to be added here

    :return: The set of commands
    """
    from sp.commands import (
        # PADNSQueryCommandSet, PADNSAnswerCommandSet, PADNSSearchCommandSet
        EnrichCommandSet, ScoreCommandSet,
        SPQLCommandSet, ThreatCheckCommandSet,
    )

    # the available initial commands
    return {
        EnrichCommandSet(),
        ScoreCommandSet(),
        # PADNSQueryCommandSet(),
        # PADNSAnswerCommandSet(),
        # PADNSSearchCommandSet(),
        SPQLCommandSet(),
        ThreatCheckCommandSet(),
    }


SPQL_COMMANDS = ["feedsearch", "websearch", "livescan"]

MULTILINE_COMMANDS = ["feedsearch", "websearch", "livescan"]

FEEDSCAN_FIELDS = [
    "domaininfo.registrar",
    "nameservers.density",
    "nameservers.nameserver",
    "domaininfo.zone",
    "ip_diversity.asns",
    "feed_scope",
    "feed_category",
    "ip_flags.vpn_tags",
    "ip_flags.proxy_tags",
    "ip_flags.is_proxy",
    "ip_flags.is_vpn",
    "datasource",
    "ip_reputation_score",
    "vendor",
    "feed",
    "feed_frequency",
    "nameservers_tags",
    "host",
    "subdomain",
    "domain",
    "domaininfo.whois_created_date",
    "ip_diversity.ip_diversity_groups",
    "ip_diversity.ip_diversity_all",
    "ip_diversity.asn_diversity",
    "domain_urls.results_summary.tranco_rank",
    "domaininfo.whois_age",
    "domaininfo.age",
    "ns_reputation.ns_reputation_max",
    "nschanges.results_summary.ns_entropy_score",
    "ns_reputation.is_parked",
    "domain_urls.results_summary.is_url_shortener",
    "domain_urls.results_summary.is_dynamic_domain",
    "domain_urls.results_summary.tranco_top10k",
    "ip_location.continent_code",
    "ip_location.country_code",
    "subnet",
    "ip_ptr",
    "asname",
    "ipv4",
    "subnet_allocation_age",
    "asn_allocation_age",
    "density",
    "asn",
    "asn_takedown_reputation_score",
    "subnet_reputation_score",
    "asn_reputation_score",
    "benign_info.known_benign",
    "sinkhole_info.known_sinkhole_ip",
    "ip_is_dsl_dynamic",
    "ip_is_tor_exit_node",
    "sp_risk_score",
    "listing_score",
    "tags",
    "first_seen_on",
    "last_seen_on",
    "type",
    "indicator",
    "indicator_hash",
    "uuid",
]

WEBSCAN_FIELDS = {
    "adtech.ads_txt",
    "adtech.ads_txt_sha256",
    "adtech.app_ads_txt",
    "adtech.app-ads_txt_sha256",
    "adtech.sellers_json",
    "adtech.sellers_json_sha256",
    "body_analysis.adsense",
    "body_analysis.adserver",
    "body_analysis.analytics",
    "body_analysis.body_sha256",
    "body_analysis.footer_sha256",
    "body_analysis.google-adstag",
    "body_analysis.google-GA4",
    "body_analysis.google-UA",
    "body_analysis.header_sha256",
    "body_analysis.ICP_license",
    "body_analysis.js_sha256",
    "body_analysis.js_ssdeep",
    "body_analysis.language",
    "body_analysis.onion",
    "body_analysis.SHV",
    "datahash",
    "domain",
    "favicon_avg",
    "favicon2_avg",
    "favicon_md5",
    "favicon_murmur3",
    "favicon_path",
    "favicon2_md5",
    "favicon2_murmur3",
    "favicon2_path",
    "favicon_urls",
    "file",
    "file_sha256",
    "geoip.asn",
    "geoip.as_org",
    "geoip.city_name",
    "geoip.continent_code",
    "geoip.country_code2",
    "geoip.country_code3",
    "geoip.country_name",
    "geoip.dma_code",
    "geoip.latitude",
    "geoip.location.lat",
    "geoip.location.lon",
    "geoip.longitude",
    "geoip.postal_code",
    "geoip.region_code",
    "geoip.region_name",
    "geoip.timezone",
    "header.cache-control",
    "header.connection",
    "header.content-length",
    "header.content-type",
    "header.etag",
    "header.refresh",
    "header.server",
    "header.x-powered-by",
    "hhv",
    "hostname",
    "html_body_murmur3",
    "html_body_length",
    "html_body_sha256",
    "html_body_similarity",
    "html_body_ssdeep",
    "htmltitle",
    "ip",
    "jarm",
    "opendirectory",
    "origin_domain",
    "origin_hostname",
    "origin_ip",
    "origin_path",
    "origin_port",
    "origin_scheme",
    "origin_url",
    "path",
    "port",
    "redirect",
    "redirect_count",
    "redirect_list",
    "redirect_to_https",
    "response",
    "scan_date",
    "scheme",
    "ssl.authority_key_id",
    "ssl.chv",
    "ssl.expired",
    "ssl.issuer.common_name",
    "ssl.issuer.country",
    "ssl.issuer.organization",
    "ssl.not_after",
    "ssl.not_before",
    "ssl.sans",
    "ssl.sans_count",
    "ssl.serial_number",
    "ssl.SHA1",
    "ssl.SHA256",
    "ssl.sigalg",
    "ssl.subject.common_name",
    "ssl.subject.country",
    "ssl.subject.names",
    "ssl.subject.organization",
    "ssl.wildcard",
    "subdomain",
    "tld",
    "url",
}
"""SPQL fields that can be used for the field parameter of webscan command"""

SERVICES_FIELDS = {
    "banner",
    "datahash",
    "fingerprints.ECDSA",
    "fingerprints.ED25519",
    "fingerprints.RSA",
    "geoip.asn",
    "geoip.as_org",
    "ip",
    "port",
    "scan_date",
    "ssl.authority_key_id",
    "ssl.chv",
    "ssl.expired",
    "ssl.issuer.common_name",
    "ssl.issuer.country",
    "ssl.issuer.organization",
    "ssl.not_after",
    "ssl.not_before",
    "ssl.sans",
    "ssl.sans_count",
    "ssl.serial_number",
    "ssl.SHA1",
    "ssl.SHA256",
    "ssl.sigalg",
    "ssl.subject.common_name",
    "ssl.subject.country",
    "ssl.subject.names",
    "ssl.subject.organization",
    "ssl.wildcard",
}

OPEN_DIRECTORY_FIELDS = {
    "dir",
    "geoip.asn",
    "geoip.as_org",
    "hostname",
    "ip",
    "last_modified",
    "name",
    "port",
    "scan_date",
    "scheme",
    "size",
}

WEBSCAN_HISTORY_FIELDS = {
    "datahash",
    "domain",
    "hostname",
    "ip",
    "origin_url",
    "scan_date",
    "scheme",
}

WEBSCAN_FAILURE_FIELDS = {
    "domain",
    "ip",
    "port",
    "reason",
    "scan_date",
    "scheme",
    "url",
}

"""SPQL data sources that can be used for the datasource parameter of webscan command"""
SPQL_DATASOURCES = {
    "webscan",
    "torscan",
    "services",
    "opendirectory",
    "webscanhistory",
}

THREATCHECK_DATASOURCES = {
    "iofa",
}

THREATCHECK_TYPES = {
    "name",
    "ip",
}
