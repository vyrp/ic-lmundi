# -*- coding: utf-8 -*-

STUDENT_CREATE_SUCCESS = 0
STUDENT_CREATE_ERROR = 1
STUDENT_UPDATE_SUCCESS = 2
STUDENT_UPDATE_ERROR = 3
STUDENT_DELETE_SUCCESS = 4
STUDENT_DELETE_ERROR = 5
STUDENT_ID_NOT_FOUND = 6
UNKNOWN_ACTION = 1000

messages = {
    STUDENT_CREATE_SUCCESS: "O aluno foi criado com sucesso.",
    STUDENT_CREATE_ERROR: "Não foi possível criar o aluno.",
    STUDENT_UPDATE_SUCCESS: "O aluno foi atualizado com sucesso.",
    STUDENT_UPDATE_ERROR: "Não foi possível atualizar o aluno.",
    STUDENT_DELETE_SUCCESS: "O aluno foi removido com sucesso.",
    STUDENT_DELETE_ERROR: "Não foi possível remover o aluno.",
    STUDENT_ID_NOT_FOUND: "Não foi possível encontrar um aluno com esse ID.",
    UNKNOWN_ACTION: "Ação não conhecida.",
}

types = {
    STUDENT_CREATE_SUCCESS: "success",
    STUDENT_CREATE_ERROR: "danger",
    STUDENT_UPDATE_SUCCESS: "success",
    STUDENT_UPDATE_ERROR: "danger",
    STUDENT_DELETE_SUCCESS: "success",
    STUDENT_DELETE_ERROR: "danger",
    STUDENT_ID_NOT_FOUND: "danger",
    UNKNOWN_ACTION: "danger",
}
