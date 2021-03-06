#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. settings.py

Basic definitions for Eurobase API

**Contents**
"""

# *credits*:      `gjacopo <jacopo.grazzini@ec.europa.eu>`_ 
# *since*:        Tue Jan  3 23:52:40 2017

import os, sys#analysis:ignore
import inspect, six
from collections import OrderedDict, Mapping
import logging

from pyrostat import metadata

#==============================================================================
# GLOBAL VARIABLES
#==============================================================================

API_HISTORY         = {'first': 1,
                       'new': 2}
API_VERSIONS        = list(API_HISTORY.values())

PACKAGE             = "pyrostat"

PROTOCOLS           = ('http', 'https', 'ftp')
"""
Recognised protocols (API, bulk downloads,...).
"""
DEF_PROTOCOL        = {API_HISTORY['first']: 'http', 
                       API_HISTORY['new']:'https'}
PROTOCOL            = DEF_PROTOCOL
"""
Default protocol used by the API.
"""
LANGS               = ('en','de','fr')
"""
Languages supported by this package.
"""
DEF_LANG            = {API_HISTORY['first']: 'en', 
                       API_HISTORY['new']: 'en'}
"""
Default language used when launching Eurostat API.
"""

EC_URL              = {API_HISTORY['first']: 'ec.europa.eu', 
                       API_HISTORY['new']: 'webgate.acceptance.ec.europa.eu'}
"""
European Commission URL.
"""
ESTAT_DOMAIN        = {API_HISTORY['first']: 'eurostat', 
                       API_HISTORY['new']: 'estat'}
"""
Eurostat domain under European Commission URL.
"""
# ESTAT_URL           = '%s://%s/%s' % (PROTOCOL, EC_URL, ESTAT_DOMAIN)
ESTAT_URL           = {t[0]: '%s/%s' % (t[1],t[2])                  \
                       for t in [[*x[0], x[1]] for x in zip(EC_URL.items(), ESTAT_DOMAIN.values())]
                       } 
"""
Eurostat complete URL.
"""

API_SUBDOMAIN       = {API_HISTORY['first']: 'wdds/rest/data',
                       API_HISTORY['new']: 'api/dissemination/sdmx'}
"""
Subdomain of Eurostat API.
"""
API_DOMAIN          = {t[0]: '%s/%s' % (t[1],t[2])                  \
                       for t in [[*x[0], x[1]] for x in zip(ESTAT_URL.items(), API_SUBDOMAIN.values())]
                       }
"""
Domain of Eurostat API.
"""
REST_VERSION        = {API_HISTORY['first']: 2.1,
                       API_HISTORY['new']: 2.1}
"""
Version of Eurostat REST API.
"""
API_PRECISION       = {API_HISTORY['first']: 1, # only available at the moment? 
                       API_HISTORY['new']: None}
"""
Precision of data fetched through Eurostat API. 
"""
API_FMTS            = {API_HISTORY['first']: ('json', 'sdmx', 'unicode'),
                       API_HISTORY['new']: ('json', 'sdmx', 'dcat')}
"""
Formats supported by Eurostat API. 
"""
API_LANGS           = {k: ('en','de','fr') for k in (1,2)}
"""
Languages supported by Eurostat API.
"""

DEF_SORT            = {API_HISTORY['first']: 1,
                       API_HISTORY['new']: None}
"""
Default sort value.
"""
DEF_FMT             = 'json'
"""
Default format of data returned by Eurostat API request.
"""

BULK_SUBDOMAIN      = 'estat-navtree-portlet-prod'
"""
Subdomain of the repository for bulk Eurostat datasets.
"""
BULK_DOMAIN         = '%s/%s' % (ESTAT_URL, BULK_SUBDOMAIN)
"""
Online repository for bulk Eurostat datasets.
"""
BULK_QUERY          = 'BulkDownloadListing'
"""
Address linking to bulk datasets.
"""
BULK_DIR            = {'dic':   'dic', 
                       'data':  'data', 
                       'base':  '',
                       'toc':   ''}
"""
Directory (address) of bulk dictionaries/datasets/metadata files.
"""
BULK_LIST           = {'dic':   'dimlist', 
                       'data':  '', 
                       'base':  '',
                       'toc':   ''}
"""
Code for dim/list data.
"""
BULK_EXTS           = {'dic':   ['dic',], 
                       'data':  ['tsv', 'sdmx'], 
                       'base':  ['txt',],
                       'toc':   ['txt', 'xml']}
"""
Extension ("format") of bulk dictionaries/datasets/metadata files.
"""
BULK_NAMES          =  {'dic':  {'name': 'Name', 'size':'Size', 'type':'Type', 'date':'Date'},
                        'data': {'name': 'Name', 'size':'Size', 'type':'Type', 'date':'Date'},
                        'base': {'data':'data', 'dic':'dic', 'label':'label'},
                        'toc':  {'title':'title', 'code':'code', 'type':'type', \
                                 'last_update':'last update of data',           \
                                 'last_change': 'last table structure change',  \
                                 'start':'data start', 'end':'data end'}}
"""
Labels used in the tables informing the bulk dictionaries/datasets/metadata files.
"""
BULK_ZIP            = {'dic':   'gz', 
                       'data':  'gz', 
                       'base':  'gz',
                       'toc':   ''}
"""
Extension ("format") of compressed bulk dictionaries/datasets/metadata files.
"""
BULK_FILES          = {'dic':   '', 
                       'data':  '', 
                       'base':  'metabase',
                       'toc':   'table_of_contents'}
"""
Generic string used for naming the bulk dictionaries/datasets/metadata files, for
instance the file storing all metadata about Eurostat datasets, or the the table 
of contents providing contents of Eurostat database.
"""

KW_DEFAULT          = 'default'
"""
"""

BS_PARSERS          = ("html.parser", "html5lib", "lxml", "xml")
"""
"""

EXCEPTIONS          = {}

LEVELS              = {'debug': logging.DEBUG,
                       'info': logging.INFO,
                       'warning': logging.WARNING,
                       'error': logging.ERROR,#     
                       'critical': logging.CRITICAL}
"""Levels of warning/errors; default level is 'debug'."""

LOG_FILENAME            = metadata.package + '.log'
"""Log file name: where warning/info messages will be output."""

#%%
#==============================================================================
# CLASSES pyroError/pyroWarning/pyroVerbose
#==============================================================================

class pyroWarning(Warning):
    """Dummy class for warnings in this package.
    
        >>> pyroWarning(warnmsg, expr=None)

    Arguments
    ---------
    warnmsg : str
        warning message to display.
        
    Keyword arguments
    -----------------
    expr : str 
        input expression in which the warning occurs; default: :data:`expr` is 
        :data:`None`.
        
    Example
    -------
    
    ::
        
        >>> pyroWarning('This is a very interesting warning');
            pyroWarning: ! This is a very interesting warning !
    """
    def __init__(self, warnmsg, expr=None):    
        self.warnmsg = warnmsg
        if expr is not None:    self.expr = expr
        else:                   self.expr = '' 
        # warnings.warn(self.msg)
        print(self)
    def __repr__(self):             return self.msg
    def __str__(self):              
        #return repr(self.msg)
        return ( 
                "! %s%s%s !" %
                (self.warnmsg, 
                 ' ' if self.warnmsg and self.expr else '',
                 self.expr
                 )
            )
                
VERBOSE             = False
    
class pyroVerbose(object):
    """Dummy class for verbose printing mode in this package.
    
    ::
    
        >>> pyroVerbose(msg, verb=True, expr=None)

    Arguments
    ---------
    msg : str
        verbose message to display.
        
    Keyword arguments
    -----------------
    verb : bool
        flag set to :data:`True` when the string :literal:`[verbose] -` is added
        in front of each verbose message displayed.
    expr : str 
        input expression in which the verbose mode is called; default: :data:`expr` is 
        :data:`None`.
        
    Example
    -------
    
    ::

        >>> pyroVerbose('The more we talk, we less we do...', verb=True);
            [verbose] - The more we talk, we less we do...
    """
    def __init__(self, msg, expr=None, verb=VERBOSE):    
        self.msg = msg
        if verb is True:
            print('\n[verbose] - %s' % self.msg)
        if expr is not None:    self.expr = expr
    #def __repr__(self):             
    #    return self.msg
    def __str__(self):              
        return repr(self.msg)
    
class pyroError(Exception):
    """Dummy class for exception raising in this package.
    
    ::
    
        >>> raise pyroError(errmsg, errtype=None, errcode=None, expr='')

    Arguments
    ---------
    errmsg : str
        message -- explanation of the error.
        
    Keyword arguments
    -----------------
    errtype : object
        error type; when :data:`errtype` is left to :data:`None`, the system tries
        to retrieve automatically the error type using :data:`sys.exc_info()`.
    errcode : (float,int)
        error code; default: :data:`errcode` is :data:`None`.
    expr : str 
        input expression in which the error occurred; default: :data:`expr` is 
        :data:`None`.
        
    Example
    -------
    
    ::
        
        >>> try:
                assert False
            except:
                raise pyroError('It is False')
            Traceback ...
            ...
            pyroError: !!! AssertionError: It is False !!!
    """
    
    def __init__(self, errmsg, errtype=None, errcode=None, expr=''):   
        self.errmsg = errmsg
        if expr is not None:        self.expr = expr
        else:                       self.expr = '' 
        if errtype is None:
            try:
                errtype = sys.exc_info()[0]
            except:
                pass
        if inspect.isclass(errtype):            self.errtype = errtype.__name__
        elif isinstance(errtype, (int,float)):  self.errtype = str(errtype)
        else:                               self.errtype = errtype
        if errcode is not None:     self.errcode = str(errcode)
        else:                       self.errcode = ''
        # super(happyError,self).__init__(self, msg)

    def __str__(self):              
        # return repr(self.msg)
        return ( 
                "!!! %s%s%s%s%s%s%s !!!" %
                (self.errtype or '', 
                 ' ' if self.errtype and self.errcode else '',
                 self.errcode or '',
                 ': ' if (self.errtype or self.errcode) and (self.errmsg or self.expr) else '',
                 self.errmsg or '', 
                 ' ' if self.errmsg and self.expr else '',
                 self.expr or '' #[' ' + self.expr if self.expr else '']
                 )
            )

#%%    
#==============================================================================
# LOGGER CLASS
#==============================================================================
    
class pyroLogger(object): 
    """Basic logger class.
    """  
    def __init__(self, **kwargs):    
        self.logger = logging.getLogger() #'logging_kinki
        if not self.logger.handlers: 
            filename = kwargs.pop('filename',LOG_FILENAME)
            self.logger.addHandler(logging.FileHandler(filename))
            self.logger.setLevel(LEVELS[kwargs.pop('level','debug')])   
    def close(self):    
        for handler in self.logger.handlers[:]:
            try:    handler.close() # FileHandler
            except: handler.flush() # StreamHandler
            self.logger.removeHandler(handler)
    def __getattr__(self, method):
        try:    return getattr(logging,method)
        except: pass
    
LOGGER = pyroLogger()
"""Logger object: where warning/info operations are defined."""

#%%    
#==============================================================================
# OBSOLETE CLASS
#==============================================================================
class pyroObsolete(object):
    """Basic class used to specify obsolete methods and/or class.
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.method_type = ( 
                'staticmethod' if isinstance(self.func, staticmethod) else
                'classmethod' if isinstance(self.func, classmethod) else
                'property' if isinstance(self.func, property) else 
                'instancemethod' # 'function'
                )
    def __call__(self, *args, **kwargs):
        
        raise IOError('Method %s is now obsolete' % self.func.__name__)
    def __repr__(self):
        return self.func.__repr__()

#%%    
#==============================================================================
# GLOBAL CLASSES/METHODS/VARIABLES
#==============================================================================

def fileexists(file):
    """Check file existence.
    """
    return os.path.exists(os.path.abspath(file))

def clean_key_method(kwargs, method):
    """Clean keyword parameters prior to be passed to a given method/function by
    deleting all the keys that are not present in the signature of the method/function.
    """
    parameters = inspect.signature(method).parameters
    keys = [key for key in kwargs.keys()                                          \
            if key not in list(parameters.keys()) or parameters[key].KEYWORD_ONLY.value==0]
    [kwargs.pop(key) for key in keys]
    return kwargs

def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    Examples
    --------
    
    ::
        
        >>> to_key_val_list([('key', 'val')])
            [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
            [('key', 'val')]
        >>> to_key_val_list('string')
            ValueError: cannot encode objects that are not 2-tuples.
    """
    if value is None:
        return None     
    elif isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')     
    elif isinstance(value, Mapping):
        value = value.items()     
    return list(value)

def merge_dict(dnew, dold, dict_class=OrderedDict):
    """Determine appropriate setting for a given request, taking into account
    the explicit setting on that request, and the setting in the session. If a
    setting is a dictionary, they will be merged together using `dict_class`
    """
    if dold is None:
        return dnew
    elif dnew is None:
        return dold
    elif not (isinstance(dold, Mapping) and isinstance(dnew, Mapping)):
        return dnew
    merged_dict = dict_class(to_key_val_list(dold))
    merged_dict.update(to_key_val_list(dnew))
    # remove keys that are set to None. Extract keys first to avoid altering
    # the dictionary during iteration.
    none_keys = [k for (k, v) in merged_dict.items() if v is None]
    for key in none_keys:
        del merged_dict[key]
    return merged_dict

def nest_dict(left, right, skip_none=False, sep='/'):
    """

    Examples
    --------
    
    ::
        
        >>> nest_dict('a', 'b')
            'a/b'
        >>> nest_dict({1:'a',2:'b'}, 'c')
            {1: 'a/c', 2: 'b/c'}
        >>> nest_dict('a', {3:'c',4:'d'})
            {3: 'a/c', 4: 'a/d'}
        >>> nest_dict({1:'a',2:'b'}, {3:'c',4:'d'})
            {1: {3: 'a/c', 4: 'a/d'}, 2: {3: 'b/c', 4: 'b/d'}}
            
    Note that the string separator (set by default to :data:`'/'` in the examples
    above, can be set to any string value:
        
    ::
        
        >>> nest_dict({1:'a',2:'b'}, {3:'c',4:'d'}, sep='++')
            {1: {3: 'a++c', 4: 'a++d'}, 2: {3: 'b++c', 4: 'b++d'}}
            
    Note also the usage of the :data:`skip_none` argument:
        
    ::
        
        >>> nest_dict({1:'a',2:'b'}, {None:'c',4:'d'})
            {1: {None: 'a/c', 4: 'a/d'}, 2: {None: 'b/c', 4: 'b/d'}}
        >>> nest_dict({1:'a',2:'b'}, {None:'c',4:'d'}, skip_none=True)
            {1: {4: 'a/d'}, 2: {4: 'b/d'}}
    """
    if left is None or right is None:
      if left is None and right is None:
          if skip_none is True: 
              return None
          else:
              return
      else:
          if skip_none is True: 
              return None
          else:
              return left or right
    elif isinstance(left, six.string_types) and isinstance(right, six.string_types):
        return  '%s%s%s' % (left, sep, right)
    elif isinstance(right, six.string_types) and isinstance(left, Mapping):
        left = left.copy()
        for k, v in left.items():
            if skip_none is True and v is None: 
                left.pop(k)
            else:
                left[k] = nest_dict(left[k], right, skip_none=skip_none, sep=sep)
        return left
    elif isinstance(left, six.string_types) and isinstance(right, Mapping):
        right = right.copy()
        for k, v in right.items():
            if skip_none is True and v is None: 
                right.pop(k)
            else:
                right[k] = nest_dict(left, right[k], skip_none=skip_none, sep=sep)
        return right
    elif isinstance(left, Mapping) and isinstance(right, Mapping):
        left = left.copy()
        for k, v in left.items():
            if skip_none is True and v is None: 
                left.pop(k)
            elif k in right:
                left[k] = nest_dict(v, right[k], skip_none=skip_none, sep=sep)
            else:
                left[k] = {kk: nest_dict(v, right[kk], skip_none=skip_none, sep=sep) \
                            for kk in right.keys() if kk is not None or skip_none is False}
        return left
    else:
        raise IOError('parameters format not supported')
