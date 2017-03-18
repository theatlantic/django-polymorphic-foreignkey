(function($) {
    var registerFk = function(input) {
        var $input = $(input);
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
            } else {
                $input.val('').trigger('change');
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
