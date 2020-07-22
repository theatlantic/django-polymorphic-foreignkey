(function($) {
    var registerFk = function(input) {
        var $input = $(input);
        var inputName = $input.attr('name');
        var inputId = $input.attr('id');
        if (inputId.indexOf('__prefix__') >= 0) {
            return;
        }
        var contentTypeId = $input.data('contentTypeId');
        var $blank = $('<option value=""/>');
        if (!contentTypeId) {
            $blank.attr('selected', 'selected');
        }
        var $select = $('<select class="polymorphic-ctypes"/>')
            .attr('id', inputId + '_ctypes')
            .attr('name', inputName + '_ctypes')
            .append($blank);

        $input.data('choices').forEach(function(choice) {
            var $option = $('<option/>').html(choice.label).attr({
                'value': choice.content_type_id,
                'data-changelist-url': choice.url
            });
            if (choice.content_type_id == contentTypeId) {
                $option.attr('selected', 'selected');
            }
            $select.append($option);
        });
        $select.data('previousValue', $select.val());

        // Bind to the focus event to store the previous value
        $select.on("focus", function(evt) {
            $select.data('previousValue', $select.val());
        });

        $select.on('change', function() {
            var $this = $(this);
            var $selected = $this.find('option:selected');
            var $input = $('#' + $this.attr('id').replace(/_ctypes$/, ''));
            var $lookup = $('#lookup_' + $input.attr('id'));
            if (!$this.val()) {
                $input.hide();
                $lookup.hide();
            } else {
                $input.show();
                $lookup.show();
                $lookup.attr('href', $selected.data('changelistUrl'));
            }
            // Clear out the existing input value
            if (!$this.data('polymorphicFkInitialized')) {
                $this.data('polymorphicFkInitialized', true);
            } else if ($this.data('previousValue') !== $this.val()) {
                // Clear out the existing input value if the content-type has changed
                $input.val('').trigger('change');
                $this.data('previousValue', $this.val());
            }
        });
        $select.insertBefore($input);
        $select.trigger('polymorphicfk:registered');
        $select.trigger('change');
    };

    $(document).ready(function() {
        $('.vForeignKeyRawIdAdminField[data-choices]').each(function() {
            registerFk(this);
        });
        $(document).on('formset:added', function(event, $row) {
            $row.find('.vForeignKeyRawIdAdminField[data-choices]').each(function() {
                registerFk(this);
            });
        });
        $(document).trigger('polymorphicfk:initialized');
    });
})(django.jQuery);
