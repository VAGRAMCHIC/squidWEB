CREATE DATABASE IF NOT EXISTS squid_logs;

CREATE TABLE squid_logs.access_log (
    event_date    Date    DEFAULT toDate(timestamp),
    timestamp     DateTime,
    response_time Float32,
    client_ip     IPv4,
    squid_status  String,
    http_status   UInt16,
    bytes_sent    UInt32,
    method        String,
    url           String,
    username      Nullable(String),
    peer_status   String,
    mime_type     String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_date)
ORDER BY (event_date, client_ip, timestamp)
TTL event_date + INTERVAL 3 MONTH;
