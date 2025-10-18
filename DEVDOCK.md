# DevDock - CareerHub Platform

## 1. Структура БД (Дополненная)

### Блок: Users (дополненный)
```json
{
  "User": {
    "id": "Integer, PK, AutoIncrement",
    "username": "String(50), Unique, NotNull",
    "email": "String(100), Unique, NotNull",
    "hashed_password": "String(255), NotNull",
    "role": "Enum('student','recruiter'), Default='student'",
    "avatar_url": "String(255), Nullable",
    "rating": "Float, Default=0.0",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: Interests (уже есть)
```json
{
  "Interest": {
    "id": "Integer, PK, AutoIncrement",
    "name": "String(50), Unique, NotNull"
  }
}
```

### Блок: Skills (уже есть)
```json
{
  "Skill": {
    "id": "Integer, PK, AutoIncrement",
    "name": "String(50), Unique, NotNull"
  }
}
```

### Блок: UserInterests (уже есть)
```json
{
  "UserInterest": {
    "id": "Integer, PK, AutoIncrement",
    "user_id": "Integer, FK->User.id",
    "interest_id": "Integer, FK->Interest.id"
  }
}
```

### Блок: UserSkills (уже есть)
```json
{
  "UserSkill": {
    "id": "Integer, PK, AutoIncrement",
    "user_id": "Integer, FK->User.id",
    "skill_id": "Integer, FK->Skill.id"
  }
}
```

### Блок: News (уже есть)
```json
{
  "News": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "author": "String(100), NotNull",
    "main_text": "Text, NotNull",
    "image_url1": "String(255), Nullable",
    "image_url2": "String(255), Nullable",
    "start_date": "DateTime, NotNull",
    "end_date": "DateTime, NotNull",
    "address": "String(255), NotNull",
    "likes_count": "Integer, Default=0",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: NewsLikes (уже есть)
```json
{
  "NewsLike": {
    "id": "Integer, PK, AutoIncrement",
    "news_id": "Integer, FK->News.id",
    "user_id": "Integer, FK->User.id",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: Cases (уже есть)
```json
{
  "Case": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "author": "String(100), NotNull",
    "main_text": "Text, NotNull",
    "image_url1": "String(255), Nullable",
    "image_url2": "String(255), Nullable",
    "start_date": "DateTime, NotNull",
    "end_date": "DateTime, NotNull",
    "address": "String(255), NotNull",
    "tags": "String(255), Nullable",
    "participants_count": "Integer, Default=0",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: CaseParticipants (уже есть)
```json
{
  "CaseParticipant": {
    "id": "Integer, PK, AutoIncrement",
    "case_id": "Integer, FK->Case.id",
    "user_id": "Integer, FK->User.id",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: Vacancies (уже есть)
```json
{
  "Vacancy": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "author": "String(100), NotNull",
    "main_text": "Text, NotNull",
    "image_url1": "String(255), Nullable",
    "image_url2": "String(255), Nullable",
    "tags": "String(255), Nullable",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: VacancyApplications (уже есть)
```json
{
  "VacancyApplication": {
    "id": "Integer, PK, AutoIncrement",
    "vacancy_id": "Integer, FK->Vacancy.id",
    "user_id": "Integer, FK->User.id",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: Clubs (новый)
```json
{
  "Club": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "description": "Text, Nullable",
    "image_url1": "String(255), Nullable",
    "image_url2": "String(255), Nullable",
    "tags": "String(255), Nullable",
    "target_audience": "String(255), Nullable",
    "members_count": "Integer, Default=0",
    "created_by_id": "Integer, FK->User.id, NotNull",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: ClubMembers (новый)
```json
{
  "ClubMember": {
    "id": "Integer, PK, AutoIncrement",
    "club_id": "Integer, FK->Club.id",
    "user_id": "Integer, FK->User.id",
    "role": "String(20), Default='member'",
    "created_at": "DateTime, Default=now()"
  }
}
```

### Блок: UserAchievements (новый - для профиля)
```json
{
  "UserAchievement": {
    "id": "Integer, PK, AutoIncrement",
    "user_id": "Integer, FK->User.id",
    "achievement": "String(255), NotNull",
    "created_at": "DateTime, Default=now()"
  }
}
```

---

## 2. Роуты с JSON схемами

### Блок: Главная (бывший Контент)
```json
{
  "GET /news": {
    "query_params": {
      "limit": "integer, optional, default=20",
      "offset": "integer, optional, default=0"
    },
    "response": [{
      "id": "integer",
      "title": "string",
      "author": "string",
      "main_text": "string",
      "image_url1": "string",
      "image_url2": "string", 
      "start_date": "string",
      "end_date": "string",
      "address": "string",
      "likes_count": "integer",
      "created_at": "string"
    }]
  },
  "POST /news/{news_id}/like": {
    "security": [{"Bearer": []}],
    "response": {
      "success": "boolean",
      "likes_count": "integer"
    }
  },
  "GET /cases": {
    "query_params": {
      "limit": "integer, optional, default=20",
      "offset": "integer, optional, default=0"
    },
    "response": [{
      "id": "integer",
      "title": "string",
      "author": "string",
      "main_text": "string",
      "image_url1": "string",
      "image_url2": "string",
      "start_date": "string",
      "end_date": "string", 
      "address": "string",
      "tags": "string",
      "participants_count": "integer",
      "created_at": "string"
    }]
  },
  "POST /cases/{case_id}/participate": {
    "security": [{"Bearer": []}],
    "response": {
      "success": "boolean",
      "participants_count": "integer"
    }
  },
  "GET /vacancies": {
    "query_params": {
      "limit": "integer, optional, default=20", 
      "offset": "integer, optional, default=0"
    },
    "response": [{
      "id": "integer",
      "title": "string",
      "author": "string",
      "main_text": "string",
      "image_url1": "string",
      "image_url2": "string",
      "tags": "string",
      "created_at": "string"
    }]
  },
  "POST /vacancies/{vacancy_id}/apply": {
    "security": [{"Bearer": []}],
    "response": {
      "success": "boolean",
      "application_id": "integer"
    }
  }
}
```

### Блок: Клубы (новый)
```json
{
  "GET /clubs": {
    "query_params": {
      "limit": "integer, optional, default=20",
      "offset": "integer, optional, default=0"
    },
    "response": [{
      "id": "integer",
      "title": "string",
      "description": "string",
      "image_url1": "string",
      "image_url2": "string",
      "tags": "string",
      "target_audience": "string",
      "members_count": "integer",
      "created_by": {"id": "integer", "username": "string"},
      "created_at": "string"
    }]
  },
  "GET /clubs/{club_id}": {
    "response": {
      "id": "integer",
      "title": "string",
      "description": "string",
      "image_url1": "string",
      "image_url2": "string",
      "tags": "string",
      "target_audience": "string",
      "members_count": "integer",
      "created_by": {"id": "integer", "username": "string"},
      "created_at": "string",
      "members": [{
        "id": "integer",
        "username": "string",
        "avatar_url": "string",
        "rating": "float"
      }]
    }
  },
  "POST /clubs/{club_id}/join": {
    "security": [{"Bearer": []}],
    "response": {
      "success": "boolean",
      "members_count": "integer"
    }
  },
  "POST /clubs/{club_id}/leave": {
    "security": [{"Bearer": []}],
    "response": {
      "success": "boolean",
      "members_count": "integer"
    }
  }
}
```

### Блок: Пользователи (обновленный профиль)
```json
{
  "GET /auth/me": {
    "security": [{"Bearer": []}],
    "response": {
      "id": "integer",
      "username": "string",
      "email": "string",
      "role": "string",
      "avatar_url": "string",
      "rating": "float",
      "achievements": ["string"],
      "skills": ["string"],
      "cases": ["string"],
      "clubs": ["string"],
      "created_at": "string"
    }
  },
  "PATCH /auth/me": {
    "security": [{"Bearer": []}],
    "request": {
      "username": "string, optional, min=3, max=50",
      "avatar_url": "string, optional"
    },
    "response": {
      "id": "integer",
      "username": "string",
      "avatar_url": "string"
    }
  }
}
```

---

## 3. Дополнительные роуты

### Блок: Администрирование (для рекрутеров)
```json
{
  "POST /news": {
    "security": [{"Bearer": []}],
    "request": {
      "title": "string, min=1, max=100",
      "author": "string, min=1, max=100",
      "main_text": "string",
      "image_url1": "string, optional",
      "image_url2": "string, optional",
      "start_date": "string",
      "end_date": "string",
      "address": "string"
    },
    "response": {
      "id": "integer",
      "title": "string"
    }
  },
  "POST /cases": {
    "security": [{"Bearer": []}],
    "request": {
      "title": "string, min=1, max=100",
      "author": "string, min=1, max=100",
      "main_text": "string",
      "image_url1": "string, optional",
      "image_url2": "string, optional",
      "start_date": "string",
      "end_date": "string",
      "address": "string",
      "tags": "string, optional"
    },
    "response": {
      "id": "integer",
      "title": "string"
    }
  },
  "POST /vacancies": {
    "security": [{"Bearer": []}],
    "request": {
      "title": "string, min=1, max=100",
      "author": "string, min=1, max=100",
      "main_text": "string",
      "image_url1": "string, optional",
      "image_url2": "string, optional",
      "tags": "string, optional"
    },
    "response": {
      "id": "integer",
      "title": "string"
    }
  }
}
```