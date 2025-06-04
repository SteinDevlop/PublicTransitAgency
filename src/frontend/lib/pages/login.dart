import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import '../config/config.dart'; // Importa la configuración
import 'package:jwt_decoder/jwt_decoder.dart';
import '/pages/administrador.dart';
import '/pages/operario.dart';
import '/pages/pasajero.dart';
import '/pages/supervisor.dart';
import '/pages/tecnico.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;
  bool _obscurePassword = true;

  // Define our color scheme
  static const primaryColor = Color(0xFF1A73E8); // Blue
  static const secondaryColor = Color(0xFF34A853); // Green accent
  static const accentColor = Color(0xFFFBBC05); // Yellow accent
  static const backgroundColor = Colors.white;
  static const cardColor = Color(0xFFF8F9FA); // Light gray/white

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    final username = _usernameController.text;
    final password = _passwordController.text;

    // Validate inputs
    if (username.isEmpty || password.isEmpty) {
      _showErrorDialog('Por favor ingresa tu ID y contraseña');
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Realizar la solicitud POST al backend usando la URL base
      final response = await http.post(
        Uri.parse('https://publictransitagency-production.up.railway.app/login/token'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'username': username,
          'password': password,
        },
      );

      setState(() {
        _isLoading = false;
      });

      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        final token =
            responseData['access_token']; // Obtén el token de la respuesta
        final scope = JwtDecoder.decode(
            token)['scope']; // Decodifica el token para obtener el scope

        print('Token obtenido: $token');
        print('Scope obtenido: $scope');

        // Navega a la página correspondiente según el scope
        if (!mounted) return;

        if (scope == 'pasajero') {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => PassengerPanel(token: token),
            ),
          );
        } else if (scope == 'operario') {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => OperarioPanel(token: token),
            ),
          );
        } else if (scope == 'supervisor') {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => SupervisorDashboard(token: token),
            ),
          );
        } else if (scope == 'administrador') {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => AdminPanel(token: token),
            ),
          );
        } else if (scope == 'mantenimiento') {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(
              builder: (context) => TecnicoPanel(token: token),
            ),
          );
        } else {
          _showErrorDialog('Rol desconocido');
        }
      } else {
        // Mostrar un mensaje de error si las credenciales son incorrectas
        _showErrorDialog('Credenciales incorrectas: ${response.body}');
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      // Manejar errores de red o del servidor
      _showErrorDialog('Ocurrió un error: $e');
    }
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.error_outline, color: Colors.red[700]),
            const SizedBox(width: 10),
            const Text('Error'),
          ],
        ),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            style: TextButton.styleFrom(
              foregroundColor: primaryColor,
            ),
            child: const Text('Cerrar'),
          ),
        ],
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        systemOverlayStyle: SystemUiOverlayStyle.light,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Stack(
        children: [
          // Background Image with Overlay
          Container(
            width: double.infinity,
            height: double.infinity,
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage('/images/bus.webp'),
                fit: BoxFit.cover,
              ),
            ),
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    primaryColor.withOpacity(0.8),
                    primaryColor.withOpacity(0.6),
                  ],
                ),
              ),
            ),
          ),

          // Login Content
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // Logo or App Title
                      const Icon(
                        Icons.directions_bus,
                        size: 80,
                        color: Colors.white,
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'Sistema de Transporte',
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        'Inicia sesión para continuar',
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 40),

                      // Login Card
                      Container(
                        width: min(size.width * 0.9, 400),
                        decoration: BoxDecoration(
                          color: cardColor,
                          borderRadius: BorderRadius.circular(16),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.1),
                              blurRadius: 20,
                              offset: const Offset(0, 10),
                            ),
                          ],
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(24),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Bienvenido',
                                style: TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF202124),
                                ),
                              ),
                              const SizedBox(height: 8),
                              const Text(
                                'Ingresa tus credenciales para acceder',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Color(0xFF5F6368),
                                ),
                              ),
                              const SizedBox(height: 24),

                              // Username Field
                              TextField(
                                controller: _usernameController,
                                decoration: InputDecoration(
                                  labelText: 'ID',
                                  hintText: 'Ingresa tu ID',
                                  prefixIcon: const Icon(
                                    Icons.person_outline,
                                    color: primaryColor,
                                  ),
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(12),
                                    borderSide: BorderSide.none,
                                  ),
                                  filled: true,
                                  fillColor: primaryColor.withOpacity(0.05),
                                  contentPadding: const EdgeInsets.symmetric(
                                    vertical: 16,
                                    horizontal: 16,
                                  ),
                                  floatingLabelBehavior:
                                      FloatingLabelBehavior.never,
                                ),
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Color(0xFF202124),
                                ),
                                keyboardType: TextInputType.text,
                                textInputAction: TextInputAction.next,
                              ),
                              const SizedBox(height: 16),

                              // Password Field
                              TextField(
                                controller: _passwordController,
                                obscureText: _obscurePassword,
                                maxLength: 12,
                                decoration: InputDecoration(
                                  labelText: 'Contraseña',
                                  hintText: 'Ingresa tu contraseña',
                                  prefixIcon: const Icon(
                                    Icons.lock_outline,
                                    color: primaryColor,
                                  ),
                                  suffixIcon: IconButton(
                                    icon: Icon(
                                      _obscurePassword
                                          ? Icons.visibility_outlined
                                          : Icons.visibility_off_outlined,
                                      color: primaryColor,
                                    ),
                                    onPressed: () {
                                      setState(() {
                                        _obscurePassword = !_obscurePassword;
                                      });
                                    },
                                  ),
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(12),
                                    borderSide: BorderSide.none,
                                  ),
                                  filled: true,
                                  fillColor: primaryColor.withOpacity(0.05),
                                  contentPadding: const EdgeInsets.symmetric(
                                    vertical: 16,
                                    horizontal: 16,
                                  ),
                                  floatingLabelBehavior:
                                      FloatingLabelBehavior.never,
                                  counterText: '',
                                ),
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Color(0xFF202124),
                                ),
                                onSubmitted: (_) => _login(),
                              ),
                              const SizedBox(height: 24),

                              // Login Button
                              SizedBox(
                                width: double.infinity,
                                height: 50,
                                child: ElevatedButton(
                                  onPressed: _isLoading ? null : _login,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: primaryColor,
                                    foregroundColor: Colors.white,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                    elevation: 0,
                                  ),
                                  child: _isLoading
                                      ? const SizedBox(
                                          width: 24,
                                          height: 24,
                                          child: CircularProgressIndicator(
                                            color: Colors.white,
                                            strokeWidth: 2,
                                          ),
                                        )
                                      : const Text(
                                          'Iniciar sesión',
                                          style: TextStyle(
                                            fontSize: 16,
                                            fontWeight: FontWeight.w600,
                                          ),
                                        ),
                                ),
                              ),

                              // Register Form
                              Align(
                                alignment: Alignment.centerRight,
                                child: TextButton(
                                  onPressed: () {
                                    Navigator.push(context, MaterialPageRoute(builder: (_) => CreateUserWidget()));
                                  },
                                  style: TextButton.styleFrom(
                                    foregroundColor: primaryColor,
                                  ),
                                  child: const Text('¿Primera Vez? Registrarme'),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 24),

                      // Footer Text
                      const Text(
                        '© 2025 Sistema de Transporte (PublicTransitAgency)',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  double min(double a, double b) {
    return a < b ? a : b;
  }
}
class CreateUserWidget extends StatefulWidget {
  const CreateUserWidget({Key? key}) : super(key: key);

  @override
  _CreateUserWidgetState createState() => _CreateUserWidgetState();
}

class _CreateUserWidgetState extends State<CreateUserWidget> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _identificacionController = TextEditingController();
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _apellidoController = TextEditingController();
  final TextEditingController _correoController = TextEditingController();
  final TextEditingController _contrasenaController = TextEditingController();
  final TextEditingController _idTarjetaController = TextEditingController();

  bool _loading = false;
  String? _responseMessage;
  bool _success = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchNextId();
  }

  Future<void> _fetchNextId() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/user/users'),
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final nextId = (data['cantidad'] ?? 0) + 1;
        setState(() {
          _idController.text = nextId.toString();
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener el siguiente ID. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión al consultar el ID.{$e}';
      });
    }
  }

  @override
  void dispose() {
    _idController.dispose();
    _identificacionController.dispose();
    _nombreController.dispose();
    _apellidoController.dispose();
    _correoController.dispose();
    _contrasenaController.dispose();
    _idTarjetaController.dispose();
    super.dispose();
  }

  Widget _buildRegisterButton() {
    return Align(
      alignment: Alignment.centerRight,
      child: TextButton(
        onPressed: () {
          // Aquí podrías navegar a otra pantalla de registro si lo deseas
        },
        style: TextButton.styleFrom(
          foregroundColor: Theme.of(context).primaryColor,
        ),
        child: const Text('¿Primera Vez? Registrarme'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Registrar Usuario')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              _buildRegisterButton(),
              const SizedBox(height: 24),
              if (_error != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 8.0),
                  child: Text(
                    _error!,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),
              TextFormField(
                controller: _idController,
                decoration: const InputDecoration(
                  labelText: 'ID (autoasignado)',
                  prefixIcon: Icon(Icons.verified_user),
                  filled: true,
                  fillColor: Color(0xFFE0E0E0), // gris claro para resaltar
                ),
                keyboardType: TextInputType.number,
                readOnly: true, // <-- Esto permite ver el valor pero no editarlo
              ),
              TextFormField(
                controller: _identificacionController,
                decoration: const InputDecoration(labelText: 'Identificación'),
                keyboardType: TextInputType.number,
                validator: (value) =>
                    value == null || value.isEmpty ? 'Campo requerido' : null,
              ),
              TextFormField(
                controller: _nombreController,
                decoration: const InputDecoration(labelText: 'Nombre'),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Campo requerido' : null,
              ),
              TextFormField(
                controller: _apellidoController,
                decoration: const InputDecoration(labelText: 'Apellido'),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Campo requerido' : null,
              ),
              TextFormField(
                controller: _correoController,
                decoration: const InputDecoration(labelText: 'Correo'),
                keyboardType: TextInputType.emailAddress,
                validator: (value) =>
                    value == null || value.isEmpty ? 'Campo requerido' : null,
              ),
              TextFormField(
                controller: _contrasenaController,
                decoration: const InputDecoration(labelText: 'Contraseña'),
                obscureText: true,
                validator: (value) =>
                    value == null || value.isEmpty ? 'Campo requerido' : null,
              ),
              TextFormField(
                controller: _idTarjetaController,
                decoration: const InputDecoration(labelText: 'ID Tarjeta'),
                keyboardType: TextInputType.number,
                validator: (value) =>
                    value == null || value.isEmpty ? 'Campo requerido' : null,
              ),
              const SizedBox(height: 16),
              const ListTile(
                title: Text('Rol de usuario'),
                subtitle: Text('Pasajero (ID = 1)'),
                leading: Icon(Icons.person),
              ),
              const ListTile(
                title: Text('Turno'),
                subtitle: Text('Ninguno (ID = 10)'),
                leading: Icon(Icons.timelapse),
              ),
              const SizedBox(height: 16),
              _loading
                  ? const Center(child: CircularProgressIndicator())
                  : ElevatedButton(
                      onPressed: () {
                        if (_formKey.currentState!.validate()) {
                          // Aquí podrías llamar a _createUser si decides habilitar el registro
                        }
                      },
                      child: const Text('Registrar Usuario'),
                    ),
              if (_responseMessage != null)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                  child: Text(
                    _responseMessage!,
                    style: TextStyle(
                      color: _success ? Colors.green : Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}