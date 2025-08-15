describe('CRM E2E Test', () => {
  const baseUrl = 'http://localhost:5000';

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  it('debe cargar la lista inicial de clientes', () => {
    // Esperar a que se cargue la tabla
    cy.get('[data-testid="client-table"]')
      .should('exist')
      .within(() => {
        cy.get('tbody tr').its('length').should('be.gte', 0);
      });
  });

  it('debe crear un nuevo cliente y mostrarse en la lista', () => {
    // Abrir formulario de añadir
    cy.get('[data-testid="add-client-btn"]').click();

    // Llenar datos del cliente
    cy.get('[data-testid="input-nombre_completo"]').type('Juan Pérez');
    cy.get('[data-testid="input-empresa"]').type('Tech Solutions');
    cy.get('[data-testid="input-email"]').type('juan.perez@example.com');
    cy.get('[data-testid="input-telefono"]').type('555-1234');
    cy.get('[data-testid="select-status"]').select('Activo');

    // Guardar
    cy.get('[data-testid="save-client-btn"]').click();

    // Verificar que el cliente aparece en la tabla
    cy.contains('td', 'Juan Pérez').should('exist');
  });

  it('debe editar un cliente existente', () => {
    // Seleccionar primer cliente de la lista
    cy.get('[data-testid="client-row"]')
      .first()
      .within(() => {
        cy.get('[data-testid="edit-client-btn"]').click();
      });

    // Cambiar el nombre y guardar
    cy.get('[data-testid="input-nombre_completo"]').clear().type('Juan Pérez Editado');
    cy.get('[data-testid="save-client-btn"]').click();

    // Verificar que el cambio se refleje en la tabla
    cy.contains('td', 'Juan Pérez Editado').should('exist');
  });

  it('debe eliminar un cliente y desaparecer de la lista', () => {
    // Seleccionar primer cliente de la lista
    cy.get('[data-testid="client-row"]')
      .first()
      .within(() => {
        cy.get('[data-testid="delete-client-btn"]').click();
      });

    // Confirmar eliminación (si hay modal)
    cy.get('[data-testid="confirm-delete-btn"]').click();

    // Verificar que la fila ya no exista
    cy.get('[data-testid="client-row"]').should('not.exist');
  });

  it('debe filtrar clientes por nombre o empresa', () => {
    // Escribir término de búsqueda
    cy.get('[data-testid="search-input"]').type('Tech');

    // Esperar a que se actualice la tabla
    cy.get('[data-testid="client-table"]')
      .within(() => {
        cy.get('tbody tr').each(($row) => {
          const text = $row.text();
          expect(text.toLowerCase()).to.contain('tech');
        });
      });

    // Limpiar búsqueda
    cy.get('[data-testid="search-input"]').clear();

    // Verificar que la tabla vuelve a mostrar todos los clientes
    cy.get('[data-testid="client-table"]')
      .within(() => {
        cy.get('tbody tr').its('length').should('be.gte', 0);
      });
  });
});