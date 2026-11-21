import enum

class ArticleStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class BlockType(enum.Enum):
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"

class TokenType(enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"