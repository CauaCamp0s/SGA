$(document).ready(function() {
    // Função para carregar associados na tabela
    function carregarAssociados() {
        $.ajax({
            type: 'GET',
            url: '/api/associados',
            success: function(response) {
                $('#tabelaAssociados').empty();
                if (Array.isArray(response)) {
                    response.forEach(function(associado) {
                        $('#tabelaAssociados').append(`
                            <tr>
                                <td>${associado.associado_id}</td>
                                <td>${associado.nome}</td>
                                <td>${associado.email}</td>
                                <td>${associado.tipo_associado}</td>
                                <td>${associado.data_inicio_associacao}</td>
                                <td>${associado.data_fim_associacao}</td>
                                <td>
                                    <button class="btn btn-danger btn-sm" onclick="excluirAssociado(${associado.associado_id})">Excluir</button>
                                </td>
                            </tr>
                        `);
                    });
                } else {
                    console.error('Resposta inválida do servidor:', response);
                }
            },
            error: function(xhr, status, error) {
                console.error('Erro ao carregar associados:', error);
                alert('Erro ao carregar associados. Verifique o console para mais detalhes.');
            }
        });
    }

    // Carregar associados ao carregar a página
    carregarAssociados();

    // Submeter formulário para adicionar novo associado
    $('#formAssociado').submit(function(e) {
        e.preventDefault();
    
        var formData = {
            nome: $('#nome').val(),
            endereco: $('#endereco').val(),
            email: $('#email').val(),
            telefone: $('#telefone').val(),
            tipo_associado: $('#tipo_associado').val(),
            data_inicio_associacao: $('#data_inicio_associacao').val(),
            data_fim_associacao: $('#data_final_associacao').val()  // Corrigir aqui também
        };
    
        console.log('Dados do formulário:', formData);
    
        // Enviar requisição AJAX para adicionar associado
        $.ajax({
            type: 'POST',
            url: '/api/associados',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                alert(response.message);
                carregarAssociados(); // Recarregar lista de associados após adicionar
                $('#formAssociado')[0].reset(); // Limpar formulário
            },
            error: function(xhr, status, error) {
                console.error('Erro ao adicionar associado:', error);
                alert('Erro ao adicionar associado. Verifique o console para mais detalhes.');
            }
        });
    });
    
    // Função para excluir um associado
    window.excluirAssociado = function(associado_id) {
        if (confirm('Tem certeza que deseja excluir este associado?')) {
            $.ajax({
                type: 'DELETE',
                url: `/api/associados/${associado_id}`,
                success: function(response) {
                    alert(response.message);
                    carregarAssociados(); // Recarregar lista de associados após exclusão
                },
                error: function(xhr, status, error) {
                    console.error('Erro ao excluir associado:', error);
                    alert('Erro ao excluir associado. Verifique o console para mais detalhes.');
                }
            });
        }
    };
});
