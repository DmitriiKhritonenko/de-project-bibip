from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import pandas as pd


class CarService:
    # Здесь немного атрибутов класса, которые помогут правильно считывать файлы с данными
    model_idx_len = 25
    model_len = 80
    car_idx_len = 50
    car_len = 100
    sales_idx_len = 40
    sales_len = 120

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        # На случай если файлы БД не созданы
        for fname in ['sales.txt', 'sales_index.txt', 'cars.txt', 'cars_index.txt', 'models.txt', 'models_index.txt']:
            with open(self.root_directory_path + fname, 'a') as f:
                pass

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # В этом и последующих заданиях сильно усложнил себе жизнь проверяя индексы на уникальность
        max_index, position = None, None
        no_conflict_flag = True
        with open(self.root_directory_path + 'models_index.txt', 'r+') as f:
            data = f.read()
            position = len(data) // self.model_idx_len
            data = [data[i * self.model_idx_len: (i+1) * self.model_idx_len].strip().split(
                ';') for i in range(position)]
            max_index = position
            for lnum, line in enumerate(data):
                key = int(line[0])
                # Проверяем есть ли модель в БД, если да - ничего не делаем. Если нет = записываем в нужное место
                if key == model.id:
                    no_conflict_flag = False
                    break
                if key > model.id and position == max_index:
                    position = lnum
                    f.seek(position * (self.model_idx_len))
                    f.write(
                        (';'.join([str(model.id), str(max_index+1)])).ljust(self.model_idx_len))
                if key > model.id and position != max_index:
                    f.write(';'.join(line).ljust(self.model_idx_len))

            if no_conflict_flag and position == max_index:
                f.write(
                    (';'.join([str(model.id), str(max_index+1)])).ljust(self.model_idx_len))

        if no_conflict_flag:
            with open(self.root_directory_path + 'models.txt', 'a') as f:
                f.write((';'.join([str(model.id), model.name, model.brand])).ljust(
                    self.model_len))
            print('model - ok')
        else:
            print('model_id already exists')

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        max_index, position = None, None
        no_conflict_flag = True
        with open(self.root_directory_path + 'cars_index.txt', 'r+') as f:
            data = f.read()
            position = len(data) // self.car_idx_len
            data = [data[i * self.car_idx_len: (i+1) * self.car_idx_len].strip().split(
                ';') for i in range(position)]
            max_index = position
            for lnum, line in enumerate(data):
                key = line[0]
                # Проверяем есть ли авто в БД, если да - ничего не делаем. Если нет = записываем в нужное место
                if key == car.vin:
                    no_conflict_flag = False
                    break
                if key > car.vin and position == max_index:
                    position = lnum
                    f.seek(position * (self.car_idx_len))
                    f.write(
                        (';'.join([car.vin, str(max_index+1)])).ljust(self.car_idx_len))
                if key > car.vin and position != max_index:
                    f.write(';'.join(line).ljust(self.car_idx_len))
            if no_conflict_flag and position == max_index:
                f.write(
                    (';'.join([car.vin, str(max_index+1)])).ljust(self.car_idx_len))

        if no_conflict_flag:
            with open(self.root_directory_path + 'cars.txt', 'a') as f:
                f.write((';'.join([car.vin, str(car.model), str(car.price), str(
                    car.date_start), car.status])).ljust(self.car_len))
            print('car - ok')
        else:
            print('car_id already exists')

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        vin = sale.index()
        idx, car_find_flag, = None, False
        sold_car = Car.model_validate(
            {'vin': vin, 'model': 0, 'price': 0, 'date_start': '2024-01-01', 'status': 'sold'})

        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            data = f.read()
            n = len(data) // self.car_idx_len
            data = [
                data[i * self.car_idx_len: (i+1) * self.car_idx_len].strip().split(';') for i in range(n)]
            for line in data:
                if vin == line[0]:
                    idx = int(line[1])-1
                    car_find_flag = True
                    break
                if vin < line[0]:
                    break
        if car_find_flag:
            print('idx=', idx)
            with open(self.root_directory_path + 'cars.txt', 'r+') as f:
                f.seek(idx * (self.car_len))
                line = f.read(self.car_len).rstrip().split(';')
                if line[4] in ['available', 'reserve']:
                    # car_not_sold = True
                    f.seek(idx * (self.car_len))
                    f.write((';'.join([vin, str(line[1]), str(line[2]), str(
                        line[3]), 'sold'])).ljust(self.car_len))
                    sold_car.model = int(line[1])
                    sold_car.price = float(line[2])
                    sold_car.date_start = line[3]
                else:
                    print(f'Car {vin} is not avalable!')
        else:
            print(f'Car {vin} not found!')

        max_index, position = None, None
        no_conflict_flag = True
        with open(self.root_directory_path + 'sales_index.txt', 'r+') as f:
            data = f.read()
            position = len(data) // self.sales_idx_len
            data = [data[i * self.sales_idx_len: (i+1) * self.sales_idx_len].strip().split(
                ';') for i in range(position)]
            max_index = position
            for lnum, line in enumerate(data):
                key = line[0]

                if key == sale.sales_number:
                    no_conflict_flag = False
                    break
                if key > sale.sales_number and position == max_index:
                    position = lnum
                    f.seek(position * (self.sales_idx_len))
                    f.write(
                        (';'.join([sale.sales_number, str(max_index+1)])).ljust(self.sales_idx_len))
                if key > sale.sales_number and position != max_index:
                    f.write(';'.join(line).ljust(self.sales_idx_len))
            if no_conflict_flag and position == max_index:
                f.write(
                    (';'.join([sale.sales_number, str(max_index+1)])).ljust(self.sales_idx_len))

        if no_conflict_flag:
            with open(self.root_directory_path + 'sales.txt', 'a') as f:
                f.write((';'.join([sale.sales_number, sale.car_vin, str(
                    sale.cost), str(sale.sales_date)])).ljust(self.sales_len))
            print('Sales - ok')
        else:
            print('sale_number already exists')
        return sold_car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        # Невероятно но факт, если делать данное задания через индексы - в тестах ошибка, напрямуую через cars - все ОК
        car_list = []
        with open(self.root_directory_path + 'cars.txt', 'r') as f:
            data = f.read(self.car_len).rstrip().split(';')
            while len(data) == 5:
                if data[4] == status:
                    car_list.append(Car.model_validate(
                        {'vin': data[0], 'model': data[1], 'price': data[2], 'date_start': str(data[3]), 'status': data[4]}))
                data = f.read(self.car_len).rstrip().split(';')
        return car_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Имитируем джойны за счет кучи вложенных открытий файлов. Читается сложно, но работать работает
        car_full_info = {'vin': vin, 'sales_date': None,
                         'sales_cost': None, 'model': 0}
        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            data = f.read(self.car_idx_len).rstrip().split(';')
            while len(data) == 2:
                if data[0] == vin:
                    car_idx = int(data[1]) - 1
                    with open(self.root_directory_path + 'cars.txt', 'r') as fsq:
                        fsq.seek(car_idx * (self.car_len))
                        car_info = fsq.read(self.car_len).rstrip().split(';')
                        car_full_info['model'] = int(car_info[1])
                        car_full_info['price'] = float(car_info[2])
                        car_full_info['date_start'] = car_info[3]
                        car_full_info['status'] = car_info[4]
                    break
                data = f.read(self.car_idx_len).rstrip().split(';')

        with open(self.root_directory_path + 'models_index.txt', 'r') as f:
            data = f.read(self.model_idx_len).rstrip().split(';')
            while len(data) == 2:
                if int(data[0]) == car_full_info['model']:
                    model_idx = int(data[1]) - 1
                    with open(self.root_directory_path + 'models.txt', 'r') as fsq:
                        fsq.seek(model_idx * (self.model_len))
                        model_info = fsq.read(
                            self.model_len).rstrip().split(';')
                        car_full_info['car_model_name'] = model_info[1]
                        car_full_info['car_model_brand'] = model_info[2]
                        del car_full_info['model']
                    break
                data = f.read(self.model_idx_len).rstrip().split(';')
        with open(self.root_directory_path + 'sales.txt', 'r') as f:
            data = f.read(self.sales_len).rstrip().split(';')
            while len(data) >= 4:
                if data[1] == vin and len(data) == 4:
                    car_full_info['sales_date'] = data[3]
                    car_full_info['sales_cost'] = data[2]
                    break
                data = f.read(self.sales_len).rstrip().split(';')

        if len(car_full_info.keys()) > 4:
            return CarFullInfo.model_validate(car_full_info)
        else:
            return None

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        # По условиям задания базы индексом хранить можно, чем и воспользуемся
        # Файл с индексами будем перезаписывать, для этого формируем промежуточный список
        cars_index_list = []
        idx = None
        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            data = f.read()
            n = len(data) // self.car_idx_len
            data = [
                data[i * self.car_idx_len: (i+1) * self.car_idx_len].strip().split(';') for i in range(n)]
            for lnum, line in enumerate(data):
                if line[0] == vin:
                    idx = int(line[1]) - 1
                else:
                    cars_index_list.append([line[0], line[1]])
        insert_flag = False
        for num, line in enumerate(cars_index_list):
            if new_vin < line[0]:
                cars_index_list.insert(num, [new_vin, str(idx + 1)])
                insert_flag = True
                break
        if insert_flag == False:
            cars_index_list.append([new_vin, str(idx + 1)])

        with open(self.root_directory_path + 'cars_index.txt', 'w') as f:
            for line in cars_index_list:
                f.write(';'.join(line).ljust(self.car_idx_len))

        with open(self.root_directory_path + 'cars.txt', 'r+') as f:
            f.seek(idx * self.car_len)
            carline = f.read(self.car_len).rstrip().split(';')
            carline[0] = new_vin
            f.seek(idx * self.car_len)
            f.write(';'.join(carline).ljust(self.car_len))
            return Car.model_validate({'vin': carline[0], 'model': carline[1], 'price': carline[2], 'date_start': str(carline[3]), 'status': carline[4]})
        return None

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        # Несмотря на всю сложность кода все предельно просто - ищем продажу, маркируем, обновляем статус авто
        vin = None
        updated_car = dict({})
        with open(self.root_directory_path + 'sales_index.txt', 'r') as f:
            data = f.read(self.sales_idx_len).rstrip().split(';')
            while len(data) == 2:
                if data[0] == sales_number:
                    idx = int(data[1]) - 1
                    with open(self.root_directory_path + 'sales.txt', 'r+') as upf:
                        upf.seek(self.sales_len * idx)
                        row4update = upf.read(
                            self.sales_len).rstrip().split(';') + ['deleted']
                        vin = row4update[1]
                        upf.seek(self.sales_len * idx)
                        upf.write(';'.join(row4update).ljust(self.sales_len))

                    with open(self.root_directory_path + 'cars_index.txt', 'r') as fsq:
                        sdata = fsq.read(self.car_idx_len).rstrip().split(';')
                        while len(sdata) == 2:
                            if vin == sdata[0]:
                                sidx = int(sdata[1]) - 1
                                with open(self.root_directory_path + 'cars.txt', 'r+') as upf:
                                    upf.seek(self.car_len*sidx)
                                    line4update = upf.read(
                                        self.car_len).rstrip().split(';')
                                    line4update[4] = 'available'
                                    upf.seek(self.car_len*sidx)
                                    upf.write(
                                        ';'.join(line4update).ljust(self.car_len))
                                    updated_car['vin'] = line4update[0]
                                    updated_car['model'] = int(line4update[1])
                                    updated_car['price'] = float(
                                        line4update[2])
                                    updated_car['date_start'] = line4update[3]
                                    updated_car['status'] = line4update[4]
                                break
                            sdata = fsq.read(
                                self.car_idx_len).rstrip().split(';')
                    break
                data = f.read(self.sales_idx_len).rstrip().split(';')
        return Car.model_validate(updated_car)

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # По условиям задания базы индексом хранить можно, чем и воспользуемся
        cars_index_dict = dict({})
        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            data = f.read()
            n = len(data) // self.car_idx_len
            data = [
                data[i * self.car_idx_len: (i+1) * self.car_idx_len].strip().split(';') for i in range(n)]
            for l in data:
                cars_index_dict[l[0]] = l[1]
        models_index_dict = dict({})
        with open(self.root_directory_path + 'models_index.txt', 'r') as f:
            data = f.read()
            n = len(data) // self.model_idx_len
            data = [
                data[i * self.model_idx_len: (i+1) * self.model_idx_len].strip().split(';') for i in range(n)]
            for l in data:
                models_index_dict[l[0]] = l[1]
        # Считаем статистику продаж по моделям
        sales_dict = {}
        with open(self.root_directory_path + 'sales.txt', 'r') as f:
            sline = f.read(self.sales_len).rstrip().split(';')
            while len(sline) >= 4:
                if len(sline) == 4:
                    current_vin = sline[1]
                    car_idx = int(cars_index_dict.get(current_vin, None)) - 1
                    with open(self.root_directory_path + 'cars.txt', 'r') as fsub:
                        fsub.seek(self.car_len * car_idx)
                        carline = fsub.read(self.car_len).rstrip().split(';')
                        car_brand_id = carline[1]

                        if car_brand_id in sales_dict.keys():
                            sales_dict[car_brand_id]['count'] += 1
                            sales_dict[car_brand_id]['cost'] += float(sline[2])
                        else:
                            sales_dict[car_brand_id] = {
                                'count': 1, 'cost': float(sline[2])}

                sline = f.read(self.sales_len).rstrip().split(';')
        # Здесь мне чуть надоело изобретать велосипеды, использовал то к чему привык - Pandas
        sales_df = pd.DataFrame([{'model': key, 'count': sales_dict[key]
                                ['count'], 'cost': sales_dict[key]['cost']} for key in sales_dict])
        sales_df = sales_df.sort_values(
            by=['count', 'cost'], ascending=[False, False])
        sales_df_srt = sales_df.head(3).reset_index(drop=True)
        # Упаковывем результат
        result_list = []
        for i in range(len(sales_df_srt)):
            midx = int(models_index_dict.get(
                sales_df_srt['model'][i], None)) - 1
            with open(self.root_directory_path + 'models.txt', 'r') as f:
                f.seek(self.model_len * midx)
                mline = f.read(self.model_len).rstrip().split(';')
                result_list.append(ModelSaleStats.model_validate(
                    {'car_model_name': mline[1], 'brand': mline[2], 'sales_number': sales_df_srt['count'][i]}))
        return result_list
