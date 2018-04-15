import json

from flask import request, jsonify
from flask_restful import abort

from app.api.rest.base import NonSecure, Secure, rest_resource

import pandas as pd
import numpy as np

from collections import namedtuple, Counter

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)

@rest_resource
class CompareDataSets(Secure):
    endpoints = ['/compare']

    def post(self):
        if request.data:
            json_payload = request.json
        else:
            return abort(400, message='Please Send Data!')

        old_data = json_payload.get('old')
        new_data = json_payload.get('new')

        if not old_data or not new_data:
            return abort(400, message="Please Send Data with 'old' and 'new' keys!")

        added_keys = list(set(new_data.keys()) - set(old_data.keys()))
        deleted_keys = list(set(old_data.keys()) - set(new_data.keys()))

        df1 = pd.DataFrame.from_dict(old_data, orient="index")
        df2 = pd.DataFrame.from_dict(new_data, orient="index")

        df1_columns = list(df1)
        df2_columns = list(df2)
        matching_columns = list(set(df1_columns) & set(df2_columns))

        merged_frame = df1.join(df2, on=None, how='left', lsuffix='_1', rsuffix='_2', sort=False)
        merged_frame = merged_frame.where((pd.notnull(merged_frame)), None)
        merged_tuples = merged_frame.itertuples(index=True, name='MergedTuple')

        changes = []
        Change = namedtuple('Change', "key field old new", verbose=False)

        for row in merged_tuples:
            for col in matching_columns:
                old_value = getattr(row, col + "_1")
                new_value = getattr(row, col + "_2")
                if old_value and new_value:
                    if old_value != new_value:
                        changes.append(Change(row.Index, col, old_value, new_value))

        keys_with_change = [c.key for c in changes]
        fields_with_change = [c.field for c in changes]

        changes = [c._asdict() for c in changes]
        changes_by_key = dict(Counter(keys_with_change))
        changes_by_field = dict(Counter(fields_with_change))

        payload = json.dumps({'added': added_keys,
                              'deleted': deleted_keys,
                              'changes': changes,
                              'changes_by_key': changes_by_key,
                              'changes_by_field': changes_by_field}, cls=NumpyEncoder)
        return json.loads(payload)
