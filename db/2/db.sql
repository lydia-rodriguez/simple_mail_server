CREATE TABLE Messages
(
  msg_id INT NOT NULL,
  sender VARCHAR NOT NULL,
  source VARCHAR NOT NULL,
  recipients VARCHAR NOT NULL,
  body VARCHAR NOT NULL,
  message_read BOOLEAN NOT NULL,
  time_received DATE NOT NULL,
  time_parsed DATE NOT NULL,
  ttl_ts FLOAT NOT NULL,
  PRIMARY KEY (msg_id)
);

CREATE TABLE Sites
(
  site_id NUMERIC NOT NULL,
  site_num INT NOT NULL,
  site_name VARCHAR NOT NULL,
  client_name VARCHAR NOT NULL,
  geo_address VARCHAR NOT NULL,
  geo_city VARCHAR NOT NULL,
  geo_state VARCHAR NOT NULL,
  geo_zipcode VARCHAR NOT NULL,
  store_phone INT NOT NULL,
  ems_type VARCHAR NOT NULL,
  commissioned_date DATE NOT NULL,
  area_sqft FLOAT NOT NULL,
  ip_address VARCHAR NOT NULL,
  geo_latitude FLOAT NOT NULL,
  geo_longitude FLOAT NOT NULL,
  wstn_primary INT NOT NULL,
  wstn_secondary INT NOT NULL,
  monitor_status VARCHAR NOT NULL,
  time_zone VARCHAR NOT NULL,
  PRIMARY KEY (site_id)
);

CREATE TABLE Alarms
(
  alarm_id INT NOT NULL,
  site_id INT NOT NULL,
  alarm_date DATE NOT NULL,
  alarm_time DATE NOT NULL,
  alarm_status VARCHAR NOT NULL,
  alarm_name VARCHAR NOT NULL,
  priority VARCHAR NOT NULL,
  ems_point VARCHAR NOT NULL,
  ems_value VARCHAR NOT NULL,
  ems_message VARCHAR NOT NULL,
  msg_id INT NOT NULL,
  site_id NUMERIC NOT NULL,
  PRIMARY KEY (alarm_id),
  FOREIGN KEY (msg_id) REFERENCES Messages(msg_id),
  FOREIGN KEY (site_id) REFERENCES Sites(site_id)
);
