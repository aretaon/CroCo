# -*- coding: utf-8 -*-

"""
Functions to read xQuest data.

"""


import numpy as np
import pandas as pd

import re

if __name__ == '__main__':
    import HelperFunctions as hf
else:
    from . import HelperFunctions as hf

def init(this_order):
    """
    Initialises the column order when called from the GUI. No function if calling directly.
    """
    global col_order
    col_order = this_order

def process_xQuest_spectrum(spec_string):
    """
    Extract rawfile name, precursor charge and scan no from xQuest spectrum
    string

    Args:
        spec_string: xQuest spectrum string
    Returns:
        str or np.nan: rawfile name
        int or np.nan: scan number
        int or np.nan: precursor charge
    """
    spectrum_pattern = re.compile('(.+)\.(\d+)\.\d+\..+\.\d+\.\d+\.(\d+)')
    if spectrum_pattern.match(spec_string):
        match = spectrum_pattern.match(spec_string)
        # rawfile, scanno, prec_ch
        return match.groups()
    else:
        return np.nan

def process_xQuest_Id(Id_string):
    """
    Extract peptide sequence of the alpha (longer) and the beta (shorter)
    peptide as well as the relative positions of the cross-links within
    these sequences from an xQuest Id-string
    
    Args:
        ID_string (str): an xQuest Id-String
    Returns:
        str or np.nan: pepseq1
        str or np.nan: pepseq2
        int or np.nan: xlink1
        int or np.nan: xlink2
    """
    Id_pattern = re.compile('(\w+)-(\w+)-a(\d+)-b(\d+)')
    if Id_pattern.match(Id_string):
        match = Id_pattern.match(Id_string)
        # pepseq1, pepseq2, xlink1, xlink2
        pepseq1, pepseq2, xlink1, xlink2 = match.groups()

        return pepseq1, pepseq2, int(xlink1), int(xlink2)
    else:
        return np.nan

def categorizexQuestType(XQType):
    """
    Extract protein name and absolute cross-link position from
    xQuest type string (xlink, loop, mono)
    
    Args:
        XQType (str): xquest type string
    Returns:
        str or np.nan: type of cross-link (inter, loop, mono)
    """

    if XQType == 'xlink':
        return 'inter'
    elif XQType in ['loop', 'looplink']:
        return 'loop'
    elif XQType in ['mono', 'monolink']:
        return 'mono'
    else:
        return np.nan

def Read(xQuest_files, col_order=None, compact=False):
    """
    Read xQuest results file and return file in xTable format.

    Args:
        xQuest_files (list): path to xQuest results file(s)
        col_order (list): List of xTable column titles that are used to sort and compress the resulting datatable
        compact (bool): Whether to compact the xTable to only those columns listed in col_order

    Returns:
        pandas.DataFrame: xTable data table
    """

    # convert to list if the input is only a single path
    if not isinstance(xQuest_files, list):
        xQuest_files = [xQuest_files]

    allData = list()

    for file in xQuest_files:

        ### Collect data and convert to pandas format
        print('Reading xQuest-file: ' + file)

        # only called if inter_file is not None
        try:
            s = pd.read_csv(hf.FSCompatiblePath(file),
                            delimiter='\t')
            allData.append(s)
        except:
            raise Exception('[xQuest Read] Failed opening file: {}'.format(file))

    xtable = pd.concat(allData)

    rename_dict = {'z':'prec_ch',
                   'Protein1':'prot1',
                   'Protein2': 'prot2',
                   'AbsPos1': 'xpos1',
                   'AbsPos2': 'xpos2',
                   'ld-Score': 'score'}

    # Copy and rename selected columns to new xquest df
    try:
        xtable.rename(index=str,
                      columns=rename_dict,
                      inplace=True)
    except Exception as e:
        raise Exception('Error during xQuest header renaming: %s' % e)

    # Extract rawfile, scanno and precursor charge from the mgf header string
    # used as Spectrum by xQuest
    xtable['rawfile'], xtable['scanno'], xtable['prec_ch'] =\
        zip(*xtable['Spectrum'].apply(process_xQuest_spectrum))

    # Extract peptide sequences and relative cross-link positions form the
    # xQuest ID-string
    xtable['pepseq1'], xtable['pepseq2'], xtable['xlink1'], xtable['xlink2'] =\
        zip(*xtable['Id'].apply(process_xQuest_Id))

    # Modifications are not defined in xQuest
    xtable['mod1'], xtable['mod2'] = "", ""

    # calculate the absolute position of the first amino acide of the resp
    # peptides
    xtable['pos1'] = xtable['xpos1'] - xtable['xlink1'] + 1
    xtable['pos2'] = xtable['xpos2'] - xtable['xlink2'] + 1

    # Assign mono
    xtable['type'] = np.vectorize(categorizexQuestType)(xtable['Type'])

    # Reassign the type for inter xlink to inter/intra/homomultimeric
    xtable.loc[xtable['type'] == 'inter', 'type'] =\
        np.vectorize(hf.categorizeInterPeptides)(xtable[xtable['type'] == 'inter']['prot1'],
                                                 xtable[xtable['type'] == 'inter']['pos1'],
                                                 xtable[xtable['type'] == 'inter']['pepseq1'],
                                                 xtable[xtable['type'] == 'inter']['prot2'],
                                                 xtable[xtable['type'] == 'inter']['pos2'],
                                                 xtable[xtable['type'] == 'inter']['pepseq1'])

    # generate an ID for every crosslink position within the protein(s)
    xtable['ID'] =\
        np.vectorize(hf.generateID)(xtable['type'], xtable['prot1'], xtable['xpos1'], xtable['prot2'], xtable['xpos2'])

    # xQuest does not incorporate decoy entries in the results table
    # but protein names can contain identifiers as reverse or decoy
    xtable['decoy'] = xtable['ID'].str.contains('reverse') |\
        xtable['ID'].str.contains('decoy')

    # the following properties cannot directly be inferred from the
    # xQuest results file
    # to avoid confusion with missing valued like np.nan, they are set to
    # UNKNOWN
    for header in ['xtype', 'modmass1', 'modpos1', 'modmass2', 'modpos2']:
        xtable[header] = 'UNKNOWN'

    # reassign dtypes for every element in the df
    # errors ignore leaves the dtype as object for every
    # non-numeric element
    xtable = xtable.apply(pd.to_numeric, errors = 'ignore')

    xtable = hf.applyColOrder(xtable, col_order, compact)

    ### Return df
    return xtable