import pandas as pd
from sklearn.ensemble import RandomForestRegressor


class PredictPrice:
    components = []
    data = '/Users/apple/PycharmProjects/dbo_website/ML_model/cars_data.xlsx'

    def __init__(self, components):
        self.components = components

    def preparing_data(self, data):
        #  Разделение признаков на категориальные и числовые
        categorical_features = [i for i in data.columns if data[i].dtype.name == 'object']
        numeric_features = [i for i in data.columns if data[i].dtype.name != 'object']

        # Произведем биномизацию данных
        data_describe = data.describe(include=[object])

        nonbinary_columns = [c for c in categorical_features if data_describe[c]['unique'] > 2]

        data_nonbinary = pd.get_dummies(data[nonbinary_columns])

        # Нормировка числовых данных
        data_numerical = data[numeric_features]
        data_numerical = (data_numerical - data_numerical.mean()) / data_numerical.std()

        data = pd.concat((data_numerical, data_nonbinary), axis=1)
        data = pd.DataFrame(data, dtype=float)

        data['Model'] = [i for i in range(len(data['Model']))]

        return data

    def train_model(self, new_data, trg):
        model = RandomForestRegressor(n_estimators=19, max_depth=55, max_features='sqrt')
        model.fit(new_data, trg)

        return model

    def predict_p(self):
        pd3 = {'Model': 2272, 'Year': self.components[0], 'Distance': self.components[1], 'Type': self.components[2],
               'Engine': self.components[3], 'Transmission': self.components[4], 'Fuel': self.components[5],
               'Gear': self.components[6], 'Power': self.components[7]}

        data = pd.read_excel(self.data)

        data['Model'] = [i for i in range(len(data['Model']))]
        trg = data['Price']
        data = data.drop(('Price'), axis=1)

        data.loc[len(data)] = pd3

        new_data = self.preparing_data(data)

        inp_data = new_data.loc[2272].to_frame().transpose()
        new_data = new_data[new_data['Model'] != 2272]

        model = self.train_model(new_data, trg)

        predicted_price = model.predict(inp_data)

        return predicted_price










# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
#
#
# class PredictPrice:
#
#     components = []
#     data = '/Users/apple/PycharmProjects/dbo_website/ML_model/cars_data.xlsx'
#
#     def __init__(self, components):
#         self.components = components
#
#     def preparing_data(self, data):
#
#         #  Разделение признаков на категориальные и числовые
#         categorical_features = [i for i in data.columns if data[i].dtype.name == 'object']
#         numeric_features = [i for i in data.columns if data[i].dtype.name != 'object']
#
#         # Произведем биномизацию данных
#         data_describe = data.describe(include=[object])
#
#         nonbinary_columns = [c for c in categorical_features if data_describe[c]['unique'] > 2]
#
#         data_nonbinary = pd.get_dummies(data[nonbinary_columns])
#
#         # Нормировка числовых данных
#         data_numerical = data[numeric_features]
#         data_numerical = (data_numerical - data_numerical.mean()) / data_numerical.std()
#
#         data = pd.concat((data_numerical, data_nonbinary), axis=1)
#         data = pd.DataFrame(data, dtype=float)
#
#         return data
#
#     def train_model(self, new_data, trg):
#         model = RandomForestRegressor(n_estimators=19, max_depth=55, max_features='sqrt')
#         model.fit(new_data, trg)
#
#         return model
#
#     def prepare_new_data(self):
#         input_data = pd.DataFrame(columns=['Model', 'Year', 'Distance', 'Type', 'Engine',
#                                            'Transmission', 'Fuel', 'Gear', 'Power'])
#
#         input_data['Model'] = 1
#         input_data['Year'] = self.components[0]
#         input_data['Distance'] = self.components[1]
#         input_data['Type'] = self.components[2]
#         input_data['Engine'] = self.components[3]
#         input_data['Transmission'] = self.components[4]
#         input_data['Fuel'] = self.components[5]
#         input_data['Gear'] = self.components[6]
#         input_data['Power'] = self.components[7]
#
#         return input_data
#
#     def predict(self):
#         data = pd.read_excel(self.data)
#
#         data['Model'] = [i for i in range(len(data['Model']))]
#         trg = data['Price']
#         data = data.drop(('Price'), axis=1)
#
#         new_data = self.preparing_data(data)
#
#         model = self.train_model(new_data, trg)
#
#         inp_data = self.prepare_new_data()
#
#         predicted_price = model.predict(inp_data)






