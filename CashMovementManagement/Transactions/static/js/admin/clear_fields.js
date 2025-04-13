document.addEventListener('DOMContentLoaded', function() {
    const fieldDependencies = {
        'id_type': {
            'fields': ['select2-id_subcategory-container', 'select2-id_category-container', 'select2-id_parent_category-container'],
            'isAutocomplete': false,
        },
        'select2-id_category-container': {
            'fields': ['select2-id_subcategory-container'],
            'isAutocomplete': true,
        },
    };


    function initFieldClearing() {
        for (const [sourceFieldId, { fields: targetFieldsIds, isAutocomplete: isAutocompleteField }] of Object.entries(fieldDependencies)) {
            const sourceField = document.getElementById(sourceFieldId);
            if (sourceField) {
                if (isAutocompleteField) {
                    sourceField.parentElement.addEventListener('click', function() {
                        clearTargetFields(targetFieldsIds);
                    });
                } else {
                    sourceField.addEventListener('change', function() {
                        clearTargetFields(targetFieldsIds);
                    });
                }
            }
        }
    }

    function clearTargetFields(targetFieldsIds) {
        targetFieldsIds.forEach(function(fieldId) {
            const field = document.getElementById(fieldId);
            if (!field) return;

            field.value = '';
            field.textContent = '';

            // Для полей с автокомплитом (django-autocomplete-light)
            // Ищем скрытое поле, которое обычно имеет name без префикса id_
            const hiddenInputName = fieldId.replace('id_', '');
            const hiddenInput = document.querySelector(`input[name="${hiddenInputName}"]`);
            if (hiddenInput) {
                hiddenInput.value = '';
            }

            // Очищаем визуальное представление Select2
            const select2Container = field.closest('.select2-container') ||
                                  field.nextElementSibling?.classList.contains('select2-container') ?
                                  field.nextElementSibling : null;

            if (select2Container) {
                // Очищаем текст в видимой части
                const renderedElement = select2Container.querySelector('.select2-selection__rendered');
                if (renderedElement) {
                    renderedElement.textContent = '';
                    renderedElement.title = '';
                }

                // Убираем крестик очистки
                const clearButton = select2Container.querySelector('.select2-selection__clear');
                if (clearButton) {
                    clearButton.style.display = 'none';
                }
            }

            // Инициируем событие change для обновления состояния
            const changeEvent = new Event('change', { bubbles: true });
            field.dispatchEvent(changeEvent);
        });
    }

    // Запускаем инициализацию с небольшой задержкой для динамических элементов
    setTimeout(initFieldClearing, 300);


    document.addEventListener('formset:added', function(event) {
        setTimeout(initFieldClearing, 100);
    });
});