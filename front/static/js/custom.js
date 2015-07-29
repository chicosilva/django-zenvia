jQuery.fn.brTelMask = function () {

    return this.each(function () {
        var el = this;
        $(el).focus(function () {
            $(el).mask("(99) 9999-9999?9");
        });

        $(el).focusout(function () {
            var phone, element;
            element = $(el);
            element.unmask();
            phone = element.val().replace(/\D/g, '');
            if (phone.length > 10) {
                element.mask("(99) 99999-999?9");
            } else {
                element.mask("(99) 9999-9999?9");
            }
        });
    });
}

$(document).ready(function () {

    $(".enviar_denuncia").on('click', function () {

        $.ajax({
            type: "GET",
            dataType: 'json',
            data: {'noticia_id': $("#noticia_id").val() },
            url: '/denuncia/',
            beforeSend: function () {
                $(".load_envio").html("<span  class='marca_texto_vermelho'> Aguarde...</span>");
            },
            success: function (response) {
                $(".load_envio").html("<span class='marca_texto_verde'>Pronto, vamos analisar o conteúdo dessa mensagem.</span>");
            },
            error: function () {
                $(".load_envio").html("<span class='marca_texto_vermelho'> Ocorreu algum erro, tente novamente</span>");
            },
            timeout: 10000
        });
        return false;
    });

    $(".enviar_teste").on('click', function () {

        $.ajax({
            type: "GET",
            dataType: 'json',
            data: $(".form_teste").serialize(),
            url: '/mensagem-teste/',
            beforeSend: function () {
                $(".load_envio").html("<span  class='marca_texto_vermelho'> Aguarde...</span>");
            },
            success: function (response) {

                if(response.sucesso){

                    $(".load_envio").html("<span class='marca_texto_verde'> SMS enviado.</span>");
                }else{

                    if(!response.texto){

                        if(form_marketing == 'codigo'){
                            $(".load_envio").html("<span class='marca_texto_vermelho'>Escolha algum código promocional</span>");
                            return false;
                        }

                        $(".load_envio").html("<span class='marca_texto_vermelho'>Escolha uma notícia</span>");
                        return false;
                    }

                    $(".load_envio").html("<span class='marca_texto_vermelho'>Ocorreu algum erro, tente novamente</span>");
                }

            },
            error: function () {
                $(".load_envio").html("<span class='marca_texto_vermelho'> Ocorreu algum erro, tente novamente</span>");
            },
            timeout: 10000
        });

    });

    $("#marcar_todos").change(function(){

        if(this.checked) {
            $('.ckecklist').prop('checked', true);
        }else{
            $('.ckecklist').prop('checked', false);
        }

    });

    $.fn.datepicker.dates['en'] = {
        days: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
        daysShort: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"],
        daysMin: ["Do", "Se", "Te", "Qua", "Qui", "Se", "Sa", "Do"],
        months: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        monthsShort: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        today: "Hoje",
        clear: "Limpar"
    };

    var SPMaskBehavior = function (val) {
            return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
        },
        spOptions = {
            onKeyPress: function (val, e, field, options) {
                field.mask(SPMaskBehavior.apply({}, arguments), options);
            }
        };

    $('#data_1 .input-group.date').datepicker({
        todayBtn: "linked",
        keyboardNavigation: false,
        format: 'dd/mm/yyyy',
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });

    var elem = document.querySelector('.js-switch');
    var switchery = new Switchery(elem, {color: '#1AB394'});

    $("#id_cep").mask('00000-000');
    $('#id_celular, #id_telefone').mask(SPMaskBehavior, spOptions);
    $("#id_data_nascimento").mask('00/00/0000');

    $("#id_cep").on('focusout', function () {

        if ($(this).val() == "" || $(this).val() == " ") {
            return false;
        }

        $.ajax({
            type: "GET",
            dataType: 'json',
            data: {'cep': $(this).val()},
            url: '/get-endereco/',
            beforeSend: function () {
                $(".lbuscacep").after(" <br> <span  class='marca_texto_vermelho'> Aguarde, configurando endereço...</span>");
            },
            success: function (response) {

                $(".marca_texto_vermelho").html("");
                $("#id_bairro").val(response.bairro_id);

                $("#id_endereco").val(response.logradouro + ", " + response.bairro + ", " + response.localidade + " - " + response.uf);

            },
            error: function () {
                $(".marca_texto_vermelho").html("");
            },
            timeout: 10000
        });

    });

    $("#receber_sms_check").on('change', function () {
        $("#form_status_notificacao").submit();
    });

    $("#id_set_mensagem_padrao").on('change', function () {
        $('#id_texto').val('');
        $('#id_texto').val(mensagens[$(this).val()]);
    });

    $("#id_codigo_promocional").on('change', function () {
        $('#id_texto').val('');
        $('#id_texto').val(mensagens[$(this).val()]);
    });

    $("#id_noticia").on('change', function () {
        $('#id_texto').val('');
        $('#id_texto').val(mensagens[$(this).val()]);
    });

    $("#id_imagem").on('change', function () {
        $('#id_texto').val('');
        $('#id_texto').val(mensagens[$(this).val()]);
    });

    $("#id_texto").counter({text: false, goal: 140});
    $("#id_title").counter({text: false, goal: 70});

    $("#id_assinatura_sms").counter({text: false, goal: 25});

    $(".codigo_t").counter({text: false, goal: 10});
    $("#id_texto_codigo").counter({text: false, goal: 110});

    $('#envia_mensagem').click(function () {
        $('#confirmar_envio').modal('hide');
        $('#form_enviar_mensagem_usuario, #enviar_mensagem_usuarios_especificos, #acao_massa').submit();
    });

    $('#btn_confirmar_remocao').click(function () {
        $('#confirmar_remocao').modal('hide');
        $('#form_remover_numeros_invalidos').submit();
    });

    var config = {
        '.chosen-select': {},
        '.chosen-select-deselect': {allow_single_deselect: true},
        '.chosen-select-no-single': {disable_search_threshold: 10},
        '.chosen-select-no-results': {no_results_text: 'Oops, nada encontrado!'},
        '.chosen-select-width': {width: "95%"}
    }
    for (var selector in config) {
        $(selector).chosen(config[selector]);
    }

    $("#id_todos").on('change', function () {
        $('#id_categoria, #id_bairro').val('');
    });

    $("#id_categoria, #id_bairro").on('change', function () {
        $('#id_todos').val('');
    });

    $('.add-row').click(function () {
        return addForm(this, 'form');
    });
    $('.delete-row').click(function () {
        return deleteForm(this, 'form');
    })

    $('#form_set input').addClass('form-control');

    $('.popup-gallery').magnificPopup({
          delegate: 'a',
          type: 'image',
          tLoading: 'Loading image #%curr%...',
          mainClass: 'mfp-img-mobile',
          gallery: {
            enabled: true,
            navigateByImgClick: true,
            preload: [0,1] // Will preload 0 - before current, and 1 after the current image
          },
          image: {
            tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'

          }
        });

});

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = $('.dynamic-form:first').clone(true).get(0);
    $(row).removeAttr('id').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');
    $(row).children().not(':last').children().each(function () {
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
    });
    $(row).find('.delete-row').click(function () {
        deleteForm(this, prefix);
    });
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn, prefix) {
    $(btn).parents('.dynamic-form').remove();
    var forms = $('.dynamic-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i = 0, formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).children().not(':last').children().each(function () {
            updateElementIndex(this, prefix, i);
        });
    }
    return false;
}