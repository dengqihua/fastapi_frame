"""
Base Orm Model
"""
import logging

from tortoise import Model, Tortoise, fields

MYSQL_KEYWORDS_UPPER = {
    "ACCESSIBLE", "ACCOUNT", "ACTION", "ADD", "AFTER", "AGAINST", "AGGREGATE",
    "ALGORITHM", "ALL", "ALTER", "ALWAYS", "ANALYSE", "ANALYZE", "AND", "ANY",
    "AS", "ASC", "ASCII", "ASENSITIVE", "AT", "AUTOEXTEND_SIZE",
    "AUTO_INCREMENT", "AVG", "AVG_ROW_LENGTH", "BACKUP", "BEFORE", "BEGIN",
    "BETWEEN", "BIGINT", "BINARY", "BINLOG", "BIT", "BLOB", "BLOCK", "BOOL",
    "BOOLEAN", "BOTH", "BTREE", "BY", "BYTE", "CACHE", "CALL", "CASCADE",
    "CASCADED", "CASE", "CATALOG_NAME", "CHAIN", "CHANGE", "CHANGED",
    "CHANNEL", "CHAR", "CHARACTER", "CHARSET", "CHECK", "CHECKSUM", "CIPHER",
    "CLASS_ORIGIN", "CLIENT", "CLOSE", "COALESCE", "CODE", "COLLATE",
    "COLLATION", "COLUMN", "COLUMNS", "COLUMN_FORMAT", "COLUMN_NAME",
    "COMMENT", "COMMIT", "COMMITTED", "COMPACT", "COMPLETION", "COMPRESSED",
    "COMPRESSION", "CONCURRENT", "CONDITION", "CONNECTION", "CONSISTENT",
    "CONSTRAINT", "CONSTRAINT_CATALOG", "CONSTRAINT_NAME", "CONSTRAINT_SCHEMA",
    "CONTAINS", "CONTEXT", "CONTINUE", "CONVERT", "CPU", "CREATE", "CROSS",
    "CUBE", "CURRENT", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP",
    "CURRENT_USER", "CURSOR", "CURSOR_NAME", "DATA", "DATABASE", "DATABASES",
    "DATAFILE", "DATE", "DATETIME", "DAY", "DAY_HOUR", "DAY_MICROSECOND",
    "DAY_MINUTE", "DAY_SECOND", "DEALLOCATE", "DEC", "DECIMAL", "DECLARE",
    "DEFAULT", "DEFAULT_AUTH", "DEFINER", "DELAYED", "DELAY_KEY_WRITE",
    "DELETE", "DESC", "DESCRIBE", "DES_KEY_FILE", "DETERMINISTIC",
    "DIAGNOSTICS", "DIRECTORY", "DISABLE", "DISCARD", "DISK", "DISTINCT",
    "DISTINCTROW", "DIV", "DO", "DOUBLE", "DROP", "DUAL", "DUMPFILE",
    "DUPLICATE", "DYNAMIC", "EACH", "ELSE", "ELSEIF", "ENABLE", "ENCLOSED",
    "ENCRYPTION", "END", "ENDS", "ENGINE", "ENGINES", "ENUM", "ERROR",
    "ERRORS", "ESCAPE", "ESCAPED", "EVENT", "EVENTS", "EVERY", "EXCHANGE",
    "EXECUTE", "EXISTS", "EXIT", "EXPANSION", "EXPIRE", "EXPLAIN", "EXPORT",
    "EXTENDED", "EXTENT_SIZE", "FALSE", "FAST", "FAULTS", "FETCH", "FIELDS",
    "FILE", "FILE_BLOCK_SIZE", "FILTER", "FIRST", "FIXED", "FLOAT", "FLOAT4",
    "FLOAT8", "FLUSH", "FOLLOWS", "FOR", "FORCE", "FOREIGN", "FORMAT", "FOUND",
    "FROM", "FULL", "FULLTEXT", "FUNCTION", "GENERAL", "GENERATED", "GEOMETRY",
    "GEOMETRYCOLLECTION", "GET", "GET_FORMAT", "GLOBAL", "GRANT", "GRANTS",
    "GROUP", "GROUP_REPLICATION", "HANDLER", "HASH", "HAVING", "HELP",
    "HIGH_PRIORITY", "HOST", "HOSTS", "HOUR", "HOUR_MICROSECOND",
    "HOUR_MINUTE", "HOUR_SECOND", "IDENTIFIED", "IF", "IGNORE",
    "IGNORE_SERVER_IDS", "IMPORT", "IN", "INDEX", "INDEXES", "INFILE",
    "INITIAL_SIZE", "INNER", "INOUT", "INSENSITIVE", "INSERT", "INSERT_METHOD",
    "INSTALL", "INSTANCE", "INT", "INT1", "INT2", "INT3", "INT4", "INT8",
    "INTEGER", "INTERVAL", "INTO", "INVOKER", "IO", "IO_AFTER_GTIDS",
    "IO_BEFORE_GTIDS", "IO_THREAD", "IPC", "IS", "ISOLATION", "ISSUER",
    "ITERATE", "JOIN", "JSON", "KEY", "KEYS", "KEY_BLOCK_SIZE", "KILL",
    "LANGUAGE", "LAST", "LEADING", "LEAVE", "LEAVES", "LEFT", "LESS", "LEVEL",
    "LIKE", "LIMIT", "LINEAR", "LINES", "LINESTRING", "LIST", "LOAD", "LOCAL",
    "LOCALTIME", "LOCALTIMESTAMP", "LOCK", "LOCKS", "LOGFILE", "LOGS", "LONG",
    "LONGBLOB", "LONGTEXT", "LOOP", "LOW_PRIORITY", "MASTER",
    "MASTER_AUTO_POSITION", "MASTER_BIND", "MASTER_CONNECT_RETRY",
    "MASTER_DELAY", "MASTER_HEARTBEAT_PERIOD", "MASTER_HOST",
    "MASTER_LOG_FILE", "MASTER_LOG_POS", "MASTER_PASSWORD", "MASTER_PORT",
    "MASTER_RETRY_COUNT", "MASTER_SERVER_ID", "MASTER_SSL", "MASTER_SSL_CA",
    "MASTER_SSL_CAPATH", "MASTER_SSL_CERT", "MASTER_SSL_CIPHER",
    "MASTER_SSL_CRL", "MASTER_SSL_CRLPATH", "MASTER_SSL_KEY",
    "MASTER_SSL_VERIFY_SERVER_CERT", "MASTER_TLS_VERSION", "MASTER_USER",
    "MATCH", "MAXVALUE", "MAX_CONNECTIONS_PER_HOUR", "MAX_QUERIES_PER_HOUR",
    "MAX_ROWS", "MAX_SIZE", "MAX_STATEMENT_TIME", "MAX_UPDATES_PER_HOUR",
    "MAX_USER_CONNECTIONS", "MEDIUM", "MEDIUMBLOB", "MEDIUMINT", "MEDIUMTEXT",
    "MEMORY", "MERGE", "MESSAGE_TEXT", "MICROSECOND", "MIDDLEINT", "MIGRATE",
    "MINUTE", "MINUTE_MICROSECOND", "MINUTE_SECOND", "MIN_ROWS", "MOD", "MODE",
    "MODIFIES", "MODIFY", "MONTH", "MULTILINESTRING", "MULTIPOINT",
    "MULTIPOLYGON", "MUTEX", "MYSQL_ERRNO", "NAME", "NAMES", "NATIONAL",
    "NATURAL", "NCHAR", "NDB", "NDBCLUSTER", "NEVER", "NEW", "NEXT", "NO",
    "NODEGROUP", "NONBLOCKING", "NONE", "NOT", "NO_WAIT", "NO_WRITE_TO_BINLOG",
    "NULL", "NUMBER", "NUMERIC", "NVARCHAR", "OFFSET", "OLD_PASSWORD", "ON",
    "ONE", "ONLY", "OPEN", "OPTIMIZE", "OPTIMIZER_COSTS", "OPTION",
    "OPTIONALLY", "OPTIONS", "OR", "ORDER", "OUT", "OUTER", "OUTFILE", "OWNER",
    "PACK_KEYS", "PAGE", "PARSER", "PARSE_GCOL_EXPR", "PARTIAL", "PARTITION",
    "PARTITIONING", "PARTITIONS", "PASSWORD", "PHASE", "PLUGIN", "PLUGINS",
    "PLUGIN_DIR", "POINT", "POLYGON", "PORT", "PRECEDES", "PRECISION",
    "PREPARE", "PRESERVE", "PREV", "PRIMARY", "PRIVILEGES", "PROCEDURE",
    "PROCESSLIST", "PROFILE", "PROFILES", "PROXY", "PURGE", "QUARTER", "QUERY",
    "QUICK", "RANGE", "READ", "READS", "READ_ONLY", "READ_WRITE", "REAL",
    "REBUILD", "RECOVER", "REDOFILE", "REDO_BUFFER_SIZE", "REDUNDANT",
    "REFERENCES", "REGEXP", "RELAY", "RELAYLOG", "RELAY_LOG_FILE",
    "RELAY_LOG_POS", "RELAY_THREAD", "RELEASE", "RELOAD", "REMOVE", "RENAME",
    "REORGANIZE", "REPAIR", "REPEAT", "REPEATABLE", "REPLACE",
    "REPLICATE_DO_DB", "REPLICATE_DO_TABLE", "REPLICATE_IGNORE_DB",
    "REPLICATE_IGNORE_TABLE", "REPLICATE_REWRITE_DB",
    "REPLICATE_WILD_DO_TABLE", "REPLICATE_WILD_IGNORE_TABLE", "REPLICATION",
    "REQUIRE", "RESET", "RESIGNAL", "RESTORE", "RESTRICT", "RESUME", "RETURN",
    "RETURNED_SQLSTATE", "RETURNS", "REVERSE", "REVOKE", "RIGHT", "RLIKE",
    "ROLLBACK", "ROLLUP", "ROTATE", "ROUTINE", "ROW", "ROWS", "ROW_COUNT",
    "ROW_FORMAT", "RTREE", "SAVEPOINT", "SCHEDULE", "SCHEMA", "SCHEMAS",
    "SCHEMA_NAME", "SECOND", "SECOND_MICROSECOND", "SECURITY", "SELECT",
    "SENSITIVE", "SEPARATOR", "SERIAL", "SERIALIZABLE", "SERVER", "SESSION",
    "SET", "SHARE", "SHOW", "SHUTDOWN", "SIGNAL", "SIGNED", "SIMPLE", "SLAVE",
    "SLOW", "SMALLINT", "SNAPSHOT", "SOCKET", "SOME", "SONAME", "SOUNDS",
    "SOURCE", "SPATIAL", "SPECIFIC", "SQL", "SQLEXCEPTION", "SQLSTATE",
    "SQLWARNING", "SQL_AFTER_GTIDS", "SQL_AFTER_MTS_GAPS", "SQL_BEFORE_GTIDS",
    "SQL_BIG_RESULT", "SQL_BUFFER_RESULT", "SQL_CACHE", "SQL_CALC_FOUND_ROWS",
    "SQL_NO_CACHE", "SQL_SMALL_RESULT", "SQL_THREAD", "SQL_TSI_DAY",
    "SQL_TSI_HOUR", "SQL_TSI_MINUTE", "SQL_TSI_MONTH", "SQL_TSI_QUARTER",
    "SQL_TSI_SECOND", "SQL_TSI_WEEK", "SQL_TSI_YEAR", "SSL", "STACKED",
    "START", "STARTING", "STARTS", "STATS_AUTO_RECALC", "STATS_PERSISTENT",
    "STATS_SAMPLE_PAGES", "STATUS", "STOP", "STORAGE", "STORED",
    "STRAIGHT_JOIN", "STRING", "SUBCLASS_ORIGIN", "SUBJECT", "SUBPARTITION",
    "SUBPARTITIONS", "SUPER", "SUSPEND", "SWAPS", "SWITCHES", "TABLE",
    "TABLES", "TABLESPACE", "TABLE_CHECKSUM", "TABLE_NAME", "TEMPORARY",
    "TEMPTABLE", "TERMINATED", "TEXT", "THAN", "THEN", "TIME", "TIMESTAMP",
    "TIMESTAMPADD", "TIMESTAMPDIFF", "TINYBLOB", "TINYINT", "TINYTEXT", "TO",
    "TRAILING", "TRANSACTION", "TRIGGER", "TRIGGERS", "TRUE", "TRUNCATE",
    "TYPE", "TYPES", "UNCOMMITTED", "UNDEFINED", "UNDO", "UNDOFILE",
    "UNDO_BUFFER_SIZE", "UNICODE", "UNINSTALL", "UNION", "UNIQUE", "UNKNOWN",
    "UNLOCK", "UNSIGNED", "UNTIL", "UPDATE", "UPGRADE", "USAGE", "USE", "USER",
    "USER_RESOURCES", "USE_FRM", "USING", "UTC_DATE", "UTC_TIME",
    "UTC_TIMESTAMP", "VALIDATION", "VALUE", "VALUES", "VARBINARY", "VARCHAR",
    "VARCHARACTER", "VARIABLES", "VARYING", "VIEW", "VIRTUAL", "WAIT",
    "WARNINGS", "WEEK", "WEIGHT_STRING", "WHEN", "WHERE", "WHILE", "WITH",
    "WITHOUT", "WORK", "WRAPPER", "WRITE", "X509", "XA", "XID", "XML", "XOR",
    "YEAR", "YEAR_MONTH", "ZEROFILL"
}
MYSQL_KEYWORDS_LOWER = {keyword.lower() for keyword in MYSQL_KEYWORDS_UPPER}
MYSQL_KEYWORDS = MYSQL_KEYWORDS_UPPER.union(MYSQL_KEYWORDS_LOWER)
logger = logging.getLogger(__name__)


class ConditionInvalid(Exception):
    """当前查询条件不支持"""

    def __init__(self, condition):
        super(ConditionInvalid, self).__init__("当前查询条件不支持", condition)


class FieldNameInvalid(Exception):
    """字段名与数据库关键字冲突"""

    def __init__(self, conflicts):
        super(FieldNameInvalid, self).__init__(f"字段名与数据库关键字冲突: {conflicts}")


class BaseOrmModel(Model):
    id = fields.IntField(pk=True)
    status = fields.IntField(default=1, description='状态')
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')

    # 字段命名检测开关
    NEED_FILED_NAME_CHECK = False
    # 查询条件检查开关
    NEED_CONDITION_CHECK = False
    # 重写此属性 配置支持的查询条件
    valid_conditions = [
        # 示例：
        # ['id'],
    ]
    # 查询条件缓存
    __valid_conditions = None

    @classmethod
    def get_valid_conditions(cls):
        if cls.__valid_conditions is None:
            cls.__valid_conditions = set(
                tuple(sorted(i)) for i in cls.valid_conditions
            )
        return cls.__valid_conditions

    @classmethod
    def check_filter_params(cls, filter_params):
        real_filter_keys = list({i.split('__')[0] for i in filter_params})
        real_condition = tuple(sorted(real_filter_keys))
        if real_condition in cls.get_valid_conditions():
            # 生产环境下，都是这 return
            return
        # 一般只有测试环境会走到这里
        filter_keys = [i.split('__')[0] for i in filter_params]
        condition = tuple(sorted(filter_keys))
        if condition not in cls.get_valid_conditions():
            raise ConditionInvalid(condition)
        logger.exception(f"{cls.__class__.__name__}:查询字端重复配置，高版本将修改为直接抛异常，请及时处理 :{condition}")

    @classmethod
    def filter(cls, *args, **kwargs):
        if cls.NEED_CONDITION_CHECK:
            cls.check_filter_params(kwargs)
        return super().filter(*args, **kwargs)

    def fields_dict(self):
        fields = self._meta.fields
        dic = {
            field: getattr(self, field)
            for field in fields
            if hasattr(self, field)
        }
        return dic

    def to_dict(self, *args, **kwargs):
        """model对外返回"""
        return self.fields_dict()

    @classmethod
    def db_conn(cls, using=None):
        if not using:
            assert cls._meta.app, f"请检查{cls._meta.db_table}表的 Meta.app 配置"
            using = cls._meta.app
        conn = Tortoise.get_connection(using)
        return conn

    @classmethod
    def write_conn(cls):
        return None

    @classmethod
    def read_conn(cls):
        return None

    @classmethod
    def set_manager(cls, manager):
        cls.manager = manager

    @classmethod
    def get_all_fields(cls):
        return cls._meta.fields

    class Meta:
        abstract = True


class CheckingModel(BaseOrmModel):
    NEED_FILED_NAME_CHECK = False
    NEED_CONDITION_CHECK = False
