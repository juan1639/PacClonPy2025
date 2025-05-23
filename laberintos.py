# ======================================================================
# 	laberintos.py (modulo que nos provee de los laberintos/escenarios)
#
# 	class arrays Laberintos Pantallas 
#-----------------------------------------------------------------------
class Pantallas:
	@staticmethod
	def get_laberinto(nivel=1):
		laberinto = None

		if (nivel == 1):
			laberinto = [
			9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
			9,5,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1,5,9,
			9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

			9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,
			9,1,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,1,9,
			9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,

			9,1,1,1,1,9,1,1,1,9,1,1,1,9,1,1,1,1,9,
			9,9,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,9,9,
			9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,

			9,1,9,9,1,9,1,9,1,9,1,9,1,9,1,9,9,1,9,
			9,1,9,9,1,9,1,9,1,9,1,9,1,9,1,9,9,1,9,
			0,1,1,1,1,9,1,1,1,0,1,1,1,9,1,1,1,1,0,

			9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
			9,5,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,5,9,
			9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
			]

		if (nivel == 2):
			laberinto = [
			9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
			9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
			9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

			9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,
			9,1,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,1,9,
			9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,

			9,1,1,1,1,9,1,1,1,9,1,1,1,1,1,1,1,1,9,
			9,9,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,9,9,
			9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,

			9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
			9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
			0,1,1,1,1,9,1,1,1,0,1,1,1,9,1,1,1,1,0,

			9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
			9,5,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,5,9,
			9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
			]

		return laberinto

