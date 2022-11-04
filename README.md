# `materials`

`materials` - модуль работы с базой данных материаллов
---
---
Поддерждиваемые функции:
	
	Получение списка  доступных материалов по наименованию группы материала:
		brands = materials.by_class(any_class)
	
	Получение списка доступных материалов по индексу группы материала:
		brands = materials.by_index(any_index)

	Получение индекса, группы и подгруппы материала:
		index, class_, subclass = materials.characteristics(any_brand)

	Получение химического состава материала:
		table = materials.chem_struct(any_brand)

	Получение твердости материала:
		table_hardness = materials.hardness(any_brand)

	Получение предела прочности материала:
		table_strength = materials.tensile_strength(any_brand)

---
Поддерждиваемые классы:	

    Класс "Материал":
        Создать класс:
            material = materials.Material()

        Показать передаваемые параметры класса:
            print(material.__doc__)

        Показать присвоенные параметры класса:
            material.show
        
        Задать настройки по умолчанию:
            material.get_default_settings

        Задать новый материал:
            material.get_material_parameters(brand = new_brand)

        Задать тип термообработки:
            material.update_heat_treatment(
                            heat_treatment = new_heat_treatment)

        Задать тверость обрабатываемого материала после термообработки
            (тврдость по Роквеллу):
            material.HRC = new_HRC

        Задать новый материал:
            material.update_workpiece(workpiece = new_workpiece)
