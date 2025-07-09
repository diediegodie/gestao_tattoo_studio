try:
    import historico.routes
    print("Importação de historico.routes OK!")
except Exception as e:
    print("ERRO ao importar historico.routes:")
    import traceback
    traceback.print_exc() 