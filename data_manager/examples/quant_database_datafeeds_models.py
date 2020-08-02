# coding: utf-8
# pylint: skip-file
from sqlalchemy import BigInteger, CHAR, Column, DateTime, Index, Integer, Numeric, SmallInteger, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_cboe_tickers = Table(
    'cboe_tickers', metadata,
    Column('id', BigInteger, nullable=False, server_default=text("nextval('datafeeds.cboe_tickers_id_seq'::regclass)")),
    Column('ticker', String(20), nullable=False, comment='name of the symbol'),
    Column('volume', BigInteger),
    schema='datafeeds'
)


class DataVendor(Base):
    __tablename__ = 'data_vendor'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('datafeeds.data_vendor_id_seq'::regclass)"))
    name = Column(String(40), nullable=False)
    data_id = Column(String(40), nullable=False)
    data_source_type = Column(String(40), nullable=False)
    data_source = Column(Text)
    created_date = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))


class EdgarCik(Base):
    __tablename__ = 'edgar_cik'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('datafeeds.edgar_cik_id_seq'::regclass)"))
    ticker = Column(String(20), nullable=False)
    cik = Column(String(10), nullable=False)
    created_date = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))


class EquitySecurityIdentifier(Base):
    __tablename__ = 'equity_security_identifier'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('datafeeds.equity_security_identifier_id_seq'::regclass)"))
    name = Column(String(100), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    created_date = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))


class Exchange(Base):
    __tablename__ = 'exchange'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('datafeeds.exchange_id_seq1'::regclass)"))
    name = Column(String(100), nullable=False)
    currency = Column(CHAR(3), nullable=False)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    update_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class NasdaqEquity(Base):
    __tablename__ = 'nasdaq_equity'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('datafeeds.nasdaq_equity_id_seq'::regclass)"))
    ticker = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    ipo_year = Column(Integer)
    sector = Column(String(100))
    industry = Column(String(100))
    exchange = Column(String(100))
    created_date = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))


class SimfinSharePrice(Base):
    __tablename__ = 'simfin_share_price'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('datafeeds.simfin_share_price_id_seq'::regclass)"))
    ticker = Column(String(20))
    simfin_id = Column(Integer, nullable=False)
    price_date = Column(DateTime(True), nullable=False)
    created_date = Column(DateTime(True), nullable=False)
    updated_date = Column(DateTime(True), nullable=False)
    open_price = Column(Numeric(19, 4))
    high_price = Column(Numeric(19, 4))
    low_price = Column(Numeric(19, 4))
    close_price = Column(Numeric(19, 4))
    adj_close_price = Column(Numeric(19, 4))
    dividend = Column(Numeric(19, 4))
    volume = Column(BigInteger)
    shares_outstanding = Column(Numeric(19, 4))


class EquitySecurityExchangeMap(Base):
    __tablename__ = 'equity_security_exchange_map'
    __table_args__ = (
        Index('ix_exchange_equity', 'exchange_id', 'equity_id'),
        {'schema': 'datafeeds'}
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('datafeeds.equity_security_exchange_map_id_seq'::regclass)"))
    exchange_id = Column(Integer, nullable=False)
    equity_id = Column(Integer, nullable=False)
    ticker = Column(String(20), nullable=False)
    created_date = Column(DateTime(True))
    last_updated = Column(DateTime(True))


class EquityPrice(Base):
    __tablename__ = 'equity_price'
    __table_args__ = {'schema': 'datafeeds'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('datafeeds.equity_price_id_seq'::regclass)"))
    data_vendor_id = Column(Integer, nullable=False)
    symbol_id = Column(Integer, nullable=False)
    price_date = Column(DateTime(True), nullable=False)
    created_date = Column(DateTime(True), nullable=False)
    last_updated_date = Column(DateTime(True), nullable=False)
    open_price = Column(Numeric(19, 4))
    high_price = Column(Numeric(19, 4))
    low_price = Column(Numeric(19, 4))
    close_price = Column(Numeric(19, 4))
    adj_close_price = Column(Numeric(19, 4))
    volume = Column(BigInteger)
