#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from codecs import BOM_UTF8


NBSP = u'\xA0'


class TsvReader:

    def read(self, tsvfile, populator):
        process = False
        for index, row in enumerate(tsvfile.readlines()):
            row = self._decode_row(row, index == 0)
            cells = [self._process(cell) for cell in self.split_row(row)]
            name = cells and cells[0].strip() or ''
            if name.startswith('*') and \
                    populator.start_table([c.replace('*','') for c in cells]):
                process = True
            elif process:
                populator.add(cells)
        populator.eof()

    def _decode_row(self, row, is_first):
        if is_first and row.startswith(BOM_UTF8):
            row = row[len(BOM_UTF8):]
        row = row.decode('UTF-8')
        if NBSP in row:
            row = row.replace(NBSP, ' ')
        return row

    @classmethod
    def split_row(cls, row):
        return row.rstrip().split('\t')

    def _process(self, cell):
        if len(cell) > 1 and cell[0] == cell[-1] == '"':
            cell = cell[1:-1].replace('""','"')
        return cell
