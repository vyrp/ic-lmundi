# -*- coding: utf-8 -*-

_iter = __import__("itertools").count(1, 1)

STUDENT_CREATE_SUCCESS = next(_iter)
STUDENT_CREATE_ERROR = next(_iter)
STUDENT_UPDATE_SUCCESS = next(_iter)
STUDENT_UPDATE_ERROR = next(_iter)
STUDENT_DELETE_SUCCESS = next(_iter)
STUDENT_DELETE_ERROR = next(_iter)
STUDENT_ID_NOT_FOUND = next(_iter)
UNKNOWN_ACTION = 1000
del _iter

messages = {
    STUDENT_CREATE_SUCCESS: u"O aluno foi criado com sucesso.",
    STUDENT_CREATE_ERROR: u"Não foi possível criar o aluno.",
    STUDENT_UPDATE_SUCCESS: u"O aluno foi atualizado com sucesso.",
    STUDENT_UPDATE_ERROR: u"Não foi possível atualizar o aluno.",
    STUDENT_DELETE_SUCCESS: u"O aluno foi removido com sucesso.",
    STUDENT_DELETE_ERROR: u"Não foi possível remover o aluno.",
    STUDENT_ID_NOT_FOUND: u"Não foi possível encontrar um aluno com esse ID.",
    UNKNOWN_ACTION: u"Ação não conhecida.",
}

types = {
    STUDENT_CREATE_SUCCESS: u"success",
    STUDENT_CREATE_ERROR: u"danger",
    STUDENT_UPDATE_SUCCESS: u"success",
    STUDENT_UPDATE_ERROR: u"danger",
    STUDENT_DELETE_SUCCESS: u"success",
    STUDENT_DELETE_ERROR: u"danger",
    STUDENT_ID_NOT_FOUND: u"danger",
    UNKNOWN_ACTION: u"danger",
}
