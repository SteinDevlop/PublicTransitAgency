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

  // Text Controllers
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _identificacionController = TextEditingController();
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _apellidoController = TextEditingController();
  final TextEditingController _correoController = TextEditingController();
  final TextEditingController _contrasenaController = TextEditingController();
  final TextEditingController _idTarjetaController = TextEditingController();

  // Focus Nodes
  final FocusNode _identificacionFocus = FocusNode();
  final FocusNode _nombreFocus = FocusNode();
  final FocusNode _apellidoFocus = FocusNode();
  final FocusNode _correoFocus = FocusNode();
  final FocusNode _contrasenaFocus = FocusNode();
  final FocusNode _idTarjetaFocus = FocusNode();

  // State Variables
  bool _loading = false;
  String? _responseMessage;
  bool _isSuccess = false;
  String? _error;
  bool _obscurePassword = true;
  int _identificacionLength = 0;
  int _passwordLength = 0;
  int _idTarjetaLength = 0;

  @override
  void initState() {
    super.initState();
    _fetchNextId();
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
    _identificacionFocus.dispose();
    _nombreFocus.dispose();
    _apellidoFocus.dispose();
    _correoFocus.dispose();
    _contrasenaFocus.dispose();
    _idTarjetaFocus.dispose();
    super.dispose();
  }

  Future<void> _fetchNextId() async {
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/user/users'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final nextId = (data['cantidad'] ?? 0) + 1;
        setState(() {
          _idController.text = nextId.toString();
        });
      } else {
        _showError('No se pudo obtener el siguiente ID');
      }
    } catch (e) {
      _showError('Error de conexión');
    }
  }

  Future<void> _crearUsuario() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _responseMessage = null;
      _error = null;
      _isSuccess = false;
    });

    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/user/create'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'ID': _idController.text.trim(),
          'Identificacion': _identificacionController.text.trim(),
          'Nombre': _nombreController.text.trim(),
          'Apellido': _apellidoController.text.trim(),
          'Correo': _correoController.text.trim(),
          'Contrasena': _contrasenaController.text.trim(),
          'IDRolUsuario': '1',
          'IDTurno': '10',
          'IDTarjeta': _idTarjetaController.text.trim(),
        },
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _responseMessage = 'Usuario registrado exitosamente';
          _isSuccess = true;
        });
        
        await _fetchNextId();
        _clearForm();
        _showSuccessMessage();
      } else {
        _showError('No se pudo crear el usuario');
      }
    } catch (e) {
      _showError('Error de conexión');
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  void _showError(String message) {
    setState(() {
      _error = message;
      _isSuccess = false;
    });
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red[700],
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _showSuccessMessage() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Usuario registrado exitosamente'),
        backgroundColor: Colors.green,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _clearForm() {
    _identificacionController.clear();
    _nombreController.clear();
    _apellidoController.clear();
    _correoController.clear();
    _contrasenaController.clear();
    _idTarjetaController.clear();
    
    setState(() {
      _identificacionLength = 0;
      _passwordLength = 0;
      _idTarjetaLength = 0;
    });
  }

  String? _validateEmail(String? value) {
    if (value == null || value.isEmpty) {
      return 'Requerido';
    }
    final emailRegex = RegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
    if (!emailRegex.hasMatch(value)) {
      return 'Email inválido';
    }
    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Requerido';
    }
    if (value.length < 6) {
      return 'Mínimo 6 caracteres';
    }
    if (value.length > 15) {
      return 'Máximo 15 caracteres';
    }
    return null;
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String label,
    TextInputType? keyboardType,
    bool obscureText = false,
    Widget? suffixIcon,
    String? Function(String?)? validator,
    void Function(String)? onChanged,
    FocusNode? focusNode,
    FocusNode? nextFocus,
    bool readOnly = false,
    int? maxLength,
    String? counterText,
    List<TextInputFormatter>? inputFormatters,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: TextFormField(
        controller: controller,
        focusNode: focusNode,
        keyboardType: keyboardType,
        obscureText: obscureText,
        readOnly: readOnly,
        maxLength: maxLength,
        inputFormatters: inputFormatters,
        decoration: InputDecoration(
          labelText: label,
          suffixIcon: suffixIcon,
          counterText: counterText,
          filled: readOnly,
          fillColor: readOnly ? Colors.grey[100] : null,
          border: const OutlineInputBorder(),
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
        validator: validator,
        onChanged: onChanged,
        onFieldSubmitted: (_) {
          if (nextFocus != null) {
            FocusScope.of(context).requestFocus(nextFocus);
          }
        },
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          SizedBox(
            width: 100,
            child: Text(
              label,
              style: const TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.grey,
              ),
            ),
          ),
          Text(value),
        ],
      ),
    );
  }

  Widget _buildStatusMessage() {
    if (_responseMessage == null && _error == null) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(top: 16),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: _isSuccess ? Colors.green[50] : Colors.red[50],
        border: Border.all(
          color: _isSuccess ? Colors.green : Colors.red,
          width: 1,
        ),
      ),
      child: Text(
        _responseMessage ?? _error ?? '',
        style: TextStyle(
          color: _isSuccess ? Colors.green[800] : Colors.red[800],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Registro de Usuario'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(1),
          child: Divider(height: 1),
        ),
      ),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildTextField(
                controller: _idController,
                label: 'ID',
                keyboardType: TextInputType.number,
                readOnly: true,
              ),
              
              _buildTextField(
                controller: _identificacionController,
                label: 'Identificación',
                keyboardType: TextInputType.number,
                maxLength: 4,
                counterText: '$_identificacionLength/4',
                focusNode: _identificacionFocus,
                nextFocus: _nombreFocus,
                inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                onChanged: (value) {
                  setState(() {
                    _identificacionLength = value.length;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) return 'Requerido';
                  if (value.length > 4) return 'Máximo 4 dígitos';
                  return null;
                },
              ),
              
              _buildTextField(
                controller: _nombreController,
                label: 'Nombre',
                focusNode: _nombreFocus,
                nextFocus: _apellidoFocus,
                validator: (value) => value == null || value.isEmpty ? 'Requerido' : null,
              ),
              
              _buildTextField(
                controller: _apellidoController,
                label: 'Apellido',
                focusNode: _apellidoFocus,
                nextFocus: _correoFocus,
                validator: (value) => value == null || value.isEmpty ? 'Requerido' : null,
              ),
              
              _buildTextField(
                controller: _correoController,
                label: 'Correo',
                keyboardType: TextInputType.emailAddress,
                focusNode: _correoFocus,
                nextFocus: _contrasenaFocus,
                validator: _validateEmail,
              ),
              
              _buildTextField(
                controller: _contrasenaController,
                label: 'Contraseña',
                obscureText: _obscurePassword,
                maxLength: 15,
                counterText: '$_passwordLength/15',
                focusNode: _contrasenaFocus,
                nextFocus: _idTarjetaFocus,
                suffixIcon: IconButton(
                  icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off),
                  onPressed: () {
                    setState(() {
                      _obscurePassword = !_obscurePassword;
                    });
                  },
                ),
                onChanged: (value) {
                  setState(() {
                    _passwordLength = value.length;
                  });
                },
                validator: _validatePassword,
              ),
              
              _buildTextField(
                controller: _idTarjetaController,
                label: 'ID Tarjeta',
                keyboardType: TextInputType.number,
                maxLength: 4,
                counterText: '$_idTarjetaLength/4',
                focusNode: _idTarjetaFocus,
                inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                onChanged: (value) {
                  setState(() {
                    _idTarjetaLength = value.length;
                  });
                },
                validator: (value) {
                  if (value == null || value.isEmpty) return 'Requerido';
                  if (value.length > 4) return 'Máximo 4 dígitos';
                  return null;
                },
              ),
              
              const SizedBox(height: 24),
              
              const Text(
                'Información del sistema',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 12),
              
              _buildInfoRow('Rol:', 'Pasajero (ID = 1)'),
              _buildInfoRow('Turno:', 'Ninguno (ID = 10)'),
              
              const SizedBox(height: 32),
              
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  onPressed: _loading ? null : _crearUsuario,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.black,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
                  child: _loading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          ),
                        )
                      : const Text('Registrar Usuario'),
                ),
              ),
              
              _buildStatusMessage(),
            ],
          ),
        ),
      ),
    );
  }
}