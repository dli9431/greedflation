describe('App', () => {
    it('renders the app', () => {
      cy.visit('/');
      cy.contains('Hello, World!');
    });
  });