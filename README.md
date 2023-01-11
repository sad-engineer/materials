# `materials`

`materials` - модуль работы с базой данных материалов
---
---
Поддерждиваемые константы:

    Список материалов по умолчанию (key - индекс класса материала):
    materials.DEFAULT_NAMES_FOR_MATERIALS[any_index]

    Описание доступных классов материалов:
        доступ по индексу класса материала:
            materials.NAMES_OF_CLASS_MATERIALS[any_index]
        доступ по классу материала:
            materials.INDEXES_OF_CLASS_MATERIALS[any_name]

    Описание типа термообработки:
        доступ по индексу типа термообработки:
            materials.NAMES_OF_HEAT_TREATMENT[any_index]
        доступ по типу термообработки:
            materials.INDEXES_OF_HEAT_TREATMENT[any_name]

    Описание типа поверхности заготовки:
        доступ по индексу типа поверхности заготовки:
            materials.NAMES_OF_WORKPIECE[any_index]
        доступ по типу поверхности заготовки:
            materials.INDEXES_OF_WORKPIECE[any_name]

    Описание переменных классов:
        доступ по строковому имени переменной:
            materials.DECODING[any_name_value]
---
Поддерждиваемые функции:
	
	Получение списка  доступных материалов по наименованию группы материала:
		brands = materials.by_class(any_class)
	
	Получение списка доступных материалов по индексу группы материала:
		brands = materials.by_index(any_index)

	Получение индекса, группы и подгруппы материала:
		index, class_, subclass = materials.characteristics(any_brand)

	Получение химического состава материала:
		dict = materials.chem_struct(any_brand)

	Получение твердости материала:
		dataframe = materials.hardness(any_brand)

	Получение предела прочности материала:
		dataframe = materials.tensile_strength(any_brand)
---
Поддерждиваемые классы:	
    
    Датакласс "MaterialData":
        Хранит модель данных "Материал"

        Создать класс:
            material_data = materials.Material()

        Показать передаваемые параметры класса:
            print(material_data)
            print(material_data.__doc__)
    _______________________________________________________________________________________________________
    
    Класс "Material" (наследует датакласс "MaterialData"):
        Наполняет модель данных "Материал" конкретными значениями конкретного материалла.
        Хранит методы работы с моделью данных, знает какими данными наполнять поля.

        Создать класс:
            material = materials.Material(brand: Optional[str] = any_brand)

        Показать передаваемые параметры класса:
            print(material)
            print(material.__doc__)
        
        Задать настройки по умолчанию:
            material.get_default_settings()

        Задать новый материал:
            material.get_material_parameters(brand = new_brand)
        
        Сбросить настройки класса на настройки по умолчанию:
            material.get_default_settings()
        
        Получить экземпляр класса с настройками по умолчанию:
            material = Material.default_material()
    _______________________________________________________________________________________________________
    
    Класс "WorkpieceMaterial" (наследует класс "Material"):
        Дополняет модель данных "Материал" новыми параметрами, необходимыми для "Заготовки".

        Создать класс:
            wmaterial = materials.WorkpieceMaterial(brand: Optional[str], 
                                                    heat_treatment: Optional[Union[str, int]],
                                                    hrc: Optional[Union[float, int]], 
                                                    workpiece: int)

        Показать передаваемые параметры класса:
            print(wmaterial)
            print(wmaterial.__doc__)
        
        Задать настройки по умолчанию:
            wmaterial.get_default_settings()

        Задать новый материал:
            wmaterial.get_material_parameters(brand = new_brand)

        Задать тип термообработки:
            wmaterial.update_heat_treatment(heat_treatment = new_heat_treatment)

        Задать тверость обрабатываемого материала после термообработки (тврдость по Роквеллу):
            wmaterial.HRC = new_HRC

        Задать новый тип поверхности заготовки:
            wmaterial.update_workpiece(workpiece = new_workpiece)
        
        Сбросить настройки класса на настройки по умолчанию:
            wmaterial.get_default_settings()
        
        Получить экземпляр класса с настройками по умолчанию:
            wmaterial = Material.default_material()
    _______________________________________________________________________________________________________
    
    Класс "Notifier" :
        Абстрактный класс. Наследовать при создании классов вывода результатов.
    _______________________________________________________________________________________________________
    
    Класс "FilePrinter" :
        Выводит результат в файл. Наследует Notifier
        
        Вывести поля материала в файл:
            по пути logs\\{time_prefix}_log.txt (time_prefix - метка времени создания отчета):
                materials.FilePrinter().log(any_material, 
                                            notifier=FilePrinter, 
                                            message='### Параметры материала ###')
            
            по пользовательскому пути:
                materials.FilePrinter().log(any_material, 
                                            notifier=FilePrinter, 
                                            message='### Параметры материала ###', 
                                            path=any_path)
    _______________________________________________________________________________________________________
    
    Класс "Logger" :
        Передает в конкретный логгер (наследник Notifier) объект вывода. 
        По умолчанию, выводит в консоль:
            materials.Logger().log(any_material)
            materials.Logger().log(any_material, message='### Параметры материала ###')
        
        Для прочих выводов отчета по обьекту, использовать кокой-нибудь наследник Notifier.
        Например:
            вывести поля материала в файл:
                FilePrinter = materials.FilePrinter
                materials.Logger().log( any_material, 
                                        notifier=FilePrinter, 
                                        message='### Параметры материала ###')
            
            вывести поля материала в файл по пользовательскому пути:
                FilePrinter = materials.FilePrinter                
                materials.Logger().log( any_material, 
                                        notifier=FilePrinter, 
                                        message='### Параметры материала ###', 
                                        path=any_path)
        
        