### Дополненная структура БД и эндпоинты для проекта

#### 1. Расширенная структура БД

**Блок: Users** (уже есть)
```json
{
  "User": {
    "id": "Integer, PK, AutoIncrement",
    "username": "String, Unique, NotNull",
    "email": "String, Unique, NotNull",
    "hashed_password": "String, NotNull",
    "created_at": "DateTime, Default=now()",
    "role": "Enum('student','recruiter'), Default='student'",
    "interests": "Relationship -> Interest (m2m)",
    "skills": "Relationship -> Skill (m2m)"
  }
}
```

**Блок: Interests**
```json
{
  "Interest": {
    "id": "Integer, PK, AutoIncrement",
    "name": "String(50), Unique, NotNull"
  }
}
```

**Блок: Skills**
```json
{
  "Skill": {
    "id": "Integer, PK, AutoIncrement", 
    "name": "String(50), Unique, NotNull"
  }
}
```

**Блок: News**
```json
{
  "News": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "author": "String(100), NotNull",
    "main_text": "Text, NotNull",
    "image_url1": "String(255)",
    "image_url2": "String(255)",
    "start_date": "DateTime, NotNull",
    "end_date": "DateTime, NotNull",
    "address": "String(255), NotNull",
    "likes_count": "Integer, Default=0",
    "created_at": "DateTime, Default=now()"
  }
}
```

**Блок: Cases**
```json
{
  "Case": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "author": "String(100), NotNull",
    "main_text": "Text, NotNull",
    "image_url1": "String(255)",
    "image_url2": "String(255)",
    "start_date": "DateTime, NotNull",
    "end_date": "DateTime, NotNull",
    "address": "String(255), NotNull",
    "tags": "String(255)",
    "participants_count": "Integer, Default=0",
    "created_at": "DateTime, Default=now()"
  },
  "CaseParticipant": {
    "id": "Integer, PK, AutoIncrement",
    "case_id": "Integer, FK->Case.id",
    "user_id": "Integer, FK->User.id",
    "created_at": "DateTime, Default=now()"
  }
}
```

**Блок: Vacancies**
```json
{
  "Vacancy": {
    "id": "Integer, PK, AutoIncrement",
    "title": "String(100), NotNull",
    "author": "String(100), NotNull", 
    "main_text": "Text, NotNull",
    "image_url1": "String(255)",
    "image_url2": "String(255)",
    "tags": "String(255)",
    "created_at": "DateTime, Default=now()"
  },
  "VacancyApplication": {
    "id": "Integer, PK, AutoIncrement",
    "vacancy_id": "Integer, FK->Vacancy.id",
    "user_id": "Integer, FK->User.id",
    "created_at": "DateTime, Default=now()"
  }
}
```

---

#### 2. Роуты с JSON схемами

**Блок: User Profile**
```json
{
  "PATCH /auth/role": {
    "security": [{"Bearer": []}],
    "request": {
      "role": "string, enum: ['student', 'recruiter']"
    },
    "response": {
      "success": "boolean",
      "role": "string"
    }
  },
  "GET /interests": {
    "response": [{
      "id": "integer",
      "name": "string"
    }]
  },
  "GET /skills": {
    "response": [{
      "id": "integer", 
      "name": "string"
    }]
  },
  "POST /user/interests": {
    "security": [{"Bearer": []}],
    "request": {
      "interest_ids": "array[integer]"
    },
    "response": {
      "success": "boolean",
      "interests": "array[{id: integer, name: string}]"
    }
  },
  "POST /user/skills": {
    "security": [{"Bearer": []}],
    "request": {
      "skill_ids": "array[integer]"
    },
    "response": {
      "success": "boolean", 
      "skills": "array[{id: integer, name: string}]"
    }
  }
}
```

**Блок: News**
```json
{
  "GET /news": {
    "query_params": {
      "limit": "integer, optional",
      "offset": "integer, optional"
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
  }
}
```

**Блок: Cases**
```json
{
  "GET /cases": {
    "query_params": {
      "limit": "integer, optional",
      "offset": "integer, optional"
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
  }
}
```

**Блок: Vacancies**
```json
{
  "GET /vacancies": {
    "query_params": {
      "limit": "integer, optional", 
      "offset": "integer, optional"
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

---