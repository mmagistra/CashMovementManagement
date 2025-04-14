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
                        setTimeout(function() {
                            clearTargetFields(sourceField, targetFieldsIds);
                        });
                    });
                } else {
                    sourceField.addEventListener('change', function() {
                        setTimeout(function() {
                            clearTargetFields(sourceField, targetFieldsIds);
                        });
                    });
                }
            }
        }
    }

    function clearTargetFields(sourceField, targetFieldsIds) {
        targetFieldsIds.forEach(function(fieldId) {
            resetDALField(fieldId);
        });
    }

    function resetDALField(fieldId) {
        // 1. Основные элементы
        const fieldName = fieldId.replace('id_', '');
        const visibleInput = document.getElementById(fieldId);
        const hiddenInput = document.querySelector(`input[name="${fieldName}"]`);
        const select2Container = visibleInput?.closest('.select2-container') ||
                               document.querySelector(`[aria-owns="select2-${fieldId}-results"]`);

        // 2. Сброс значений
        if (visibleInput) {
            visibleInput.value = '';
            visibleInput.dispatchEvent(new Event('change', { bubbles: true }));
        }

        if (hiddenInput) {
            hiddenInput.value = '';
            hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
        }

        // 3. Обработка Select2 (если используется)
        if (select2Container) {
            // Вариант 1: через jQuery (если подключен)
            if (typeof jQuery !== 'undefined' && jQuery.fn.select2) {
                jQuery(`#${fieldId}`).val(null).trigger('change');
            }
            // Вариант 2: чистый JS
            else {
                const selection = select2Container.querySelector('.select2-selection__rendered');
                if (selection) {
                    selection.innerHTML = '<span class="select2-selection__placeholder">Выберите значение</span>';
                }
                const clearBtn = select2Container.querySelector('.select2-selection__clear');
                if (clearBtn) clearBtn.click();
            }
        }

        // 4. Специфичные для DAL элементы
        const dalWrapper = document.querySelector(`[data-autocomplete-light-function="select2"][id$="-wrapper"]`);
        if (dalWrapper) {
            dalWrapper.dataset.select2Value = '[]';
        }

        // 5. Дополнительные события
        const event = new CustomEvent('autocompleteLightChoiceReset', {
            bubbles: true,
            detail: { fieldName: fieldName }
        });
        if (visibleInput) visibleInput.dispatchEvent(event);
    }

    // Запускаем инициализацию с небольшой задержкой для динамических элементов
    setTimeout(initFieldClearing, 300);


    document.addEventListener('formset:added', function(event) {
        setTimeout(initFieldClearing, 100);
    });
});