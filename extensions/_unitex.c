#include <Python.h>
#include "UnitexLibIO.h"

static char unitex_docstring[] =
	"This module provides some usefull C function to work with the Unitex library.";
static char unitex_get_vfs_file_list_docstring[] =
	"This function converts a C array of string (char**) into a Python list.";

static PyObject *unitex_get_vfs_file_list(PyObject *self, PyObject *args);

PyObject *unitex_get_vfs_file_list(PyObject *self, PyObject *args) {
	char *filename;
	if (!PyArg_ParseTuple(args, "s", &filename))
		return NULL;

	char **array=GetUnitexFileList(filename);
	if (array==NULL)
		return PyList_New(0);

	unsigned int size = 0;
	while ((*(array + size))!=NULL) {
		size ++;
	}

	PyObject *list = PyList_New(size);
	for (unsigned int i = 0; i != size; ++i) {
		PyList_SET_ITEM(list, i, PyUnicode_FromString(array[i]));
	}

	char **array_walk=array;
	while ((*array_walk)!=NULL) {
		free(*array_walk);
		array_walk++;
	}
	free(array);

	return list;
}

static PyMethodDef unitex_methods[] = {
	{"unitex_get_vfs_file_list", unitex_get_vfs_file_list, METH_VARARGS, unitex_get_vfs_file_list_docstring},
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
