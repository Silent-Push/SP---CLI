import os
from dotenv import load_dotenv

load_dotenv()

CRLF = "\r\n"
API_URL = os.environ.get(
    "SILENT_PUSH_API_URL", "https://app.silentpush.com/api/v1/merge-api/"
)
API_KEY = os.environ.get("SILENT_PUSH_API_KEY")

if API_URL is None:
    raise EnvironmentError(
        "Please set the Silent Push API URL in your environment.\n"
        '\texport SILENT_PUSH_API_URL="'
        'https://app.silentpush.com/api/v1/merge-api/"'
    )

if API_KEY is None:
    raise EnvironmentError(
        "Please set your Silent Push API key in your environment.\n"
        '\texport SILENT_PUSH_API_KEY="YOUR-API-KEY"'
    )


def get_initial_commands():
    from sp.commands import (
        EnrichCommandSet,
        ScoreCommandSet,
    )

    # the available initial commands
    return {
        EnrichCommandSet(),
        ScoreCommandSet(),
    }

# SPQL fields
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
    "ssl.wildcard"
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
    "size"
}

WEBSCAN_HISTORY_FIELDS = {
    "datahash",
    "domain",
    "hostname",
    "ip",
    "origin_url",
    "scan_date",
    "scheme"
}

WEBSCAN_FAILURE_FIELDS = {
    "domain",
    "ip",
    "port",
    "reason",
    "scan_date",
    "scheme",
    "url"
}

SPQL_DATASOURCES = {
    "webscan",
    "torscan",
    "services",
    "opendirectory",
    "webscanhistory",
}
