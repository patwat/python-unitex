#include <Python.h>

#include "AbstractFilePlugCallback.h"
#include "UnitexTool.h"
#include "UnitexLibIO.h"

#if defined(UNITEX_HAVING_PERSISTANCE_INTERFACE) && (!(defined(UNITEX_PREVENT_USING_PERSISTANCE_INTERFACE)))
#include "PersistenceInterface.h"
#endif

#ifdef HAS_UNITEX_NAMESPACE
using namespace unitex;
#endif

static char unitex_docstring[] =
	"This module provides some usefull C function to work with the Unitex library.";



/************************
 * UNITEX TOOL FUNCTION *
 ************************/

/* 'unitex_tool' function*/
static char unitex_tool_docstring[] =
	"This function launches an Unitex command.";
static PyObject *unitex_tool(PyObject *self, PyObject *args);

PyObject *unitex_tool(PyObject *self, PyObject *args) {
	char *command;
	if (!PyArg_ParseTuple(args, "s", &command))
		return NULL;

	unsigned int ret;
	ret = UnitexTool_public_run_string(command);

	return Py_BuildValue("i", ret);
}



/*************************
 * PERSISTENCE FUNCTIONS *
 *************************/

/*'unitex_load_persistent_dictionary' function*/
static char unitex_load_persistent_dictionary_docstring[] =
	"This function loads a dictionary in the persistent space.";
static PyObject *unitex_load_persistent_dictionary(PyObject *self, PyObject *args);

PyObject *unitex_load_persistent_dictionary(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;
	PyObject *result = NULL;

	size_t length = strlen(path)+0x200;

	char *persistent_path = (char*)malloc(length+1);
	if (persistent_path == NULL) {
		return NULL;
	}

	if (persistence_public_load_dictionary(path, persistent_path, length)) {
		result = Py_BuildValue("s", persistent_path);
	}
	free(persistent_path);

	return result;
}

/*'unitex_load_persistent_fst2' function*/
static char unitex_load_persistent_fst2_docstring[] =
	"This function loads a fst2 in the persistent space.";
static PyObject *unitex_load_persistent_fst2(PyObject *self, PyObject *args);

PyObject *unitex_load_persistent_fst2(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;
	PyObject *result = NULL;

	size_t length = strlen(path)+0x200;

	char *persistent_path = (char*)malloc(length+1);
	if (persistent_path == NULL) {
		return NULL;
	}

	if (persistence_public_load_fst2(path, persistent_path, length)) {
		result = Py_BuildValue("s", persistent_path);
	}
	free(persistent_path);

	return result;
}

/*'unitex_load_persistent_alphabet' function*/
static char unitex_load_persistent_alphabet_docstring[] =
	"This function loads an alphabet in the persistent space.";
static PyObject *unitex_load_persistent_alphabet(PyObject *self, PyObject *args);

PyObject *unitex_load_persistent_alphabet(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;
	PyObject *result = NULL;

	size_t length = strlen(path)+0x200;

	char *persistent_path = (char*)malloc(length+1);
	if (persistent_path == NULL) {
		return NULL;
	}

	if (persistence_public_load_alphabet(path, persistent_path, length)) {
		result = Py_BuildValue("s", persistent_path);
	}
	free(persistent_path);

	return result;
}



/*'unitex_free_persistent_dictionary' function*/
static char unitex_free_persistent_dictionary_docstring[] =
	"This function removes a dictionary from the persistent space.";
static PyObject *unitex_free_persistent_dictionary(PyObject *self, PyObject *args);

PyObject *unitex_free_persistent_dictionary(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	persistence_public_unload_dictionary(path);

	Py_RETURN_NONE;
}

/*'unitex_free_persistent_fst2' function*/
static char unitex_free_persistent_fst2_docstring[] =
	"This function removes a fst2 from the persistent space.";
static PyObject *unitex_free_persistent_fst2(PyObject *self, PyObject *args);

PyObject *unitex_free_persistent_fst2(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	persistence_public_unload_fst2(path);

	Py_RETURN_NONE;
}

/*'unitex_free_persistent_alphabet' function*/
static char unitex_free_persistent_alphabet_docstring[] =
	"This function removes an alphabet from the persistent space.";
static PyObject *unitex_free_persistent_alphabet(PyObject *self, PyObject *args);

PyObject *unitex_free_persistent_alphabet(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	persistence_public_unload_alphabet(path);

	Py_RETURN_NONE;
}



/*'unitex_is_persistent_dictionary' function*/
static char unitex_is_persistent_dictionary_docstring[] =
	"This function checks if a dictionary is in the persistent space.";
static PyObject *unitex_is_persistent_dictionary(PyObject *self, PyObject *args);

PyObject *unitex_is_persistent_dictionary(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	unsigned int ret;
	ret = persistence_public_is_persisted_dictionary_filename(path);

	return Py_BuildValue("i", ret);
}

/*'unitex_is_persistent_fst2' function*/
static char unitex_is_persistent_fst2_docstring[] =
	"This function checks if a fst2 is in the persistent space.";
static PyObject *unitex_is_persistent_fst2(PyObject *self, PyObject *args);

PyObject *unitex_is_persistent_fst2(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	unsigned int ret;
	ret = persistence_public_is_persisted_fst2_filename(path);

	return Py_BuildValue("i", ret);
}

/*'unitex_is_persistent_alphabet' function*/
static char unitex_is_persistent_alphabet_docstring[] =
	"This function checks if an alphabet is in the persistent space.";
static PyObject *unitex_is_persistent_alphabet(PyObject *self, PyObject *args);

PyObject *unitex_is_persistent_alphabet(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	unsigned int ret;
	ret = persistence_public_is_persisted_alphabet_filename(path);

	return Py_BuildValue("i", ret);
}



/*****************
 * I/O FUNCTIONS *
 *****************/

/* 'unitex_enable_stdout' function*/
static char unitex_enable_stdout_docstring[] =
	"This function enable the standard output.";
static PyObject *unitex_enable_stdout(PyObject *self, PyObject *noarg);

PyObject *unitex_enable_stdout(PyObject *self, PyObject *noarg) {
	enum stdwrite_kind swk = stdwrite_kind_out;

	unsigned int ret;
	ret = SetStdWriteCB(swk, 0, NULL, NULL);

	return Py_BuildValue("i", ret);
}

/* 'unitex_enable_stderr' function*/
static char unitex_enable_stderr_docstring[] =
	"This function enable the error output.";
static PyObject *unitex_enable_stderr(PyObject *self, PyObject *noarg);

PyObject *unitex_enable_stderr(PyObject *self, PyObject *noarg) {
	enum stdwrite_kind swk = stdwrite_kind_err;

	unsigned int ret;
	ret = SetStdWriteCB(swk, 0, NULL, NULL);

	return Py_BuildValue("i", ret);
}

/* 'unitex_disable_stdout' function*/
static char unitex_disable_stdout_docstring[] =
	"This function disable the standard output.";
static PyObject *unitex_disable_stdout(PyObject *self, PyObject *noarg);

PyObject *unitex_disable_stdout(PyObject *self, PyObject *noarg) {
	enum stdwrite_kind swk = stdwrite_kind_out;

	unsigned int ret;
	ret = SetStdWriteCB(swk, 1, NULL, NULL);

	return Py_BuildValue("i", ret);
}

/* 'unitex_disable_stderr' function*/
static char unitex_disable_stderr_docstring[] =
	"This function disable the error output.";
static PyObject *unitex_disable_stderr(PyObject *self, PyObject *noarg);

PyObject *unitex_disable_stderr(PyObject *self, PyObject *noarg) {
	enum stdwrite_kind swk = stdwrite_kind_err;

	unsigned int ret;
	ret = SetStdWriteCB(swk, 1, NULL, NULL);

	return Py_BuildValue("i", ret);
}

/* 'unitex_cp' function*/
static char unitex_cp_docstring[] =
	"This function copies a file to the (virtual) filesystem.";
static PyObject *unitex_cp(PyObject *self, PyObject *args);

PyObject *unitex_cp(PyObject *self, PyObject *args) {
	char *source_path;
	char *target_path;
	if (!PyArg_ParseTuple(args, "ss", &source_path, &target_path))
		return NULL;

	unsigned int ret;
	ret = CopyUnitexFile(source_path, target_path);

	return Py_BuildValue("i", ret);
}

/* 'unitex_rm' function*/
static char unitex_rm_docstring[] =
	"This function removes a file from the (virtual) filesystem.";
static PyObject *unitex_rm(PyObject *self, PyObject *args);

PyObject *unitex_rm(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	unsigned int ret;
	ret = RemoveUnitexFile(path);

	return Py_BuildValue("i", ret);
}

/* 'unitex_mv' function*/
static char unitex_mv_docstring[] =
	"This function renames (and potentially moves) a (virtual) file.";
static PyObject *unitex_mv(PyObject *self, PyObject *args);

PyObject *unitex_mv(PyObject *self, PyObject *args) {
	char *old_path;
	char *new_path;
	if (!PyArg_ParseTuple(args, "ss", &old_path, &new_path))
		return NULL;

	unsigned int ret;
	ret = RenameUnitexFile(old_path, new_path);

	return Py_BuildValue("i", ret);
}

/* 'unitex_mkdir' function*/
static char unitex_mkdir_docstring[] =
	"This function creates a directory on the disk.";
static PyObject *unitex_mkdir(PyObject *self, PyObject *args);

PyObject *unitex_mkdir(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	unsigned int ret;
	ret = CreateUnitexFolder(path);

	return Py_BuildValue("i", ret);
}

/* 'unitex_rmdir' function*/
static char unitex_rmdir_docstring[] =
	"This function removes a directory from disk (and all its content).";
static PyObject *unitex_rmdir(PyObject *self, PyObject *args);

PyObject *unitex_rmdir(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	unsigned int ret;
	ret = RemoveUnitexFolder(path);

	return Py_BuildValue("i", ret);
}

/* 'unitex_ls' function*/
static char unitex_ls_docstring[] =
	"This function list (disk or virtual) directory contents.";
static PyObject *unitex_ls(PyObject *self, PyObject *args);

PyObject *unitex_ls(PyObject *self, PyObject *args) {
	char *path;
	if (!PyArg_ParseTuple(args, "s", &path))
		return NULL;

	char **_file_list=GetUnitexFileList(path);
	if (_file_list==NULL)
		return PyList_New(0);

	unsigned int size = 0;
	while ((*(_file_list + size))!=NULL) {
		size ++;
	}

	PyObject *file_list = PyList_New(size);
	for (unsigned int i = 0; i != size; ++i) {
		PyList_SET_ITEM(file_list, i, PyUnicode_FromString(_file_list[i]));
	}

	char **_file_list_walk=_file_list;
	while ((*_file_list_walk)!=NULL) {
		free(*_file_list_walk);
		_file_list_walk++;
	}
	free(_file_list);

	return file_list;
}

static PyMethodDef unitex_methods[] = {
	/*Unitex Tool function*/
	{"unitex_tool", unitex_tool, METH_VARARGS, unitex_tool_docstring},

	/*Persistence functions*/
	{"unitex_load_persistent_dictionary", unitex_load_persistent_dictionary, METH_VARARGS, unitex_load_persistent_dictionary_docstring},
	{"unitex_load_persistent_fst2", unitex_load_persistent_fst2, METH_VARARGS, unitex_load_persistent_fst2_docstring},
	{"unitex_load_persistent_alphabet", unitex_load_persistent_alphabet, METH_VARARGS, unitex_load_persistent_alphabet_docstring},
	{"unitex_free_persistent_dictionary", unitex_free_persistent_dictionary, METH_VARARGS, unitex_free_persistent_dictionary_docstring},
	{"unitex_free_persistent_fst2", unitex_free_persistent_fst2, METH_VARARGS, unitex_free_persistent_fst2_docstring},
	{"unitex_free_persistent_alphabet", unitex_free_persistent_alphabet, METH_VARARGS, unitex_free_persistent_alphabet_docstring},
	{"unitex_is_persistent_dictionary", unitex_is_persistent_dictionary, METH_VARARGS, unitex_is_persistent_dictionary_docstring},
	{"unitex_is_persistent_fst2", unitex_is_persistent_fst2, METH_VARARGS, unitex_is_persistent_fst2_docstring},
	{"unitex_is_persistent_alphabet", unitex_is_persistent_alphabet, METH_VARARGS, unitex_is_persistent_alphabet_docstring},

	/*I/O functions*/
	{"unitex_enable_stdout", unitex_enable_stdout, METH_NOARGS, unitex_enable_stdout_docstring},
	{"unitex_disable_stdout", unitex_disable_stdout, METH_NOARGS, unitex_disable_stdout_docstring},
	{"unitex_enable_stderr", unitex_enable_stderr, METH_NOARGS, unitex_enable_stderr_docstring},
	{"unitex_disable_stderr", unitex_disable_stderr, METH_NOARGS, unitex_disable_stderr_docstring},
	{"unitex_cp", unitex_cp, METH_VARARGS, unitex_cp_docstring},
	{"unitex_rm", unitex_rm, METH_VARARGS, unitex_rm_docstring},
	{"unitex_mv", unitex_mv, METH_VARARGS, unitex_mv_docstring},
	{"unitex_mkdir", unitex_mkdir, METH_VARARGS, unitex_mkdir_docstring},
	{"unitex_rmdir", unitex_rmdir, METH_VARARGS, unitex_rmdir_docstring},
	{"unitex_ls", unitex_ls, METH_VARARGS, unitex_ls_docstring},

	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef unitexdef = {
	PyModuleDef_HEAD_INIT,
	"_unitex",
	unitex_docstring,
	-1,
	unitex_methods
};

PyMODINIT_FUNC PyInit__unitex(void) {
	PyObject *module = PyModule_Create(&unitexdef);

	if (module == NULL)
		return NULL;
	return module;
}
