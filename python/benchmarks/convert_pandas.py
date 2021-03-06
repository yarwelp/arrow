# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import numpy as np
import pandas as pd
import pyarrow as pa


class PandasConversionsBase(object):
    def setup(self, n, dtype):
        if dtype == 'float64_nans':
            arr = np.arange(n).astype('float64')
            arr[arr % 10 == 0] = np.nan
        else:
            arr = np.arange(n).astype(dtype)
        self.data = pd.DataFrame({'column': arr})


class PandasConversionsToArrow(PandasConversionsBase):
    param_names = ('size', 'dtype')
    params = ((10, 10 ** 6), ('int64', 'float64', 'float64_nans', 'str'))

    def time_from_series(self, n, dtype):
        pa.Table.from_pandas(self.data)


class PandasConversionsFromArrow(PandasConversionsBase):
    param_names = ('size', 'dtype')
    params = ((10, 10 ** 6), ('int64', 'float64', 'float64_nans', 'str'))

    def setup(self, n, dtype):
        super(PandasConversionsFromArrow, self).setup(n, dtype)
        self.arrow_data = pa.Table.from_pandas(self.data)

    def time_to_series(self, n, dtype):
        self.arrow_data.to_pandas()
