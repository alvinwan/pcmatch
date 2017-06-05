var renderer, scene, camera, stats;

var particles1, particles2, uniforms, grid;

var PARTICLE_SIZE = 20;

init();
animate();

function initGrid(scene) {
  grid = new THREE.GridHelper( 1000, 20 );
  grid.setColors( 0xffffff, 0xffffff );
  scene.add( grid );
}

function initParticlesForTemplate(template_name, offset) {
  var vertices = templates[template_name];

  var positions = new Float32Array( vertices.length * 3 );
  var colors = new Float32Array( vertices.length * 3 );
  var sizes = new Float32Array( vertices.length );

  var vertex;
  var color = new THREE.Color();

  for ( var i = 0, l = vertices.length; i < l; i ++ ) {

    vertex = vertices[ i ];
    positions[i * 3] = vertex.x;
    positions[i * 3 + 1] = vertex.z;
    positions[i * 3 + 2] = vertex.y;

    color.setHSL( offset + 0.1 * ( i / l ), 1.0, 0.5 );
    color.toArray( colors, i * 3 );

    sizes[ i ] = PARTICLE_SIZE * 0.5;

  }

  var geometry = new THREE.BufferGeometry();
  geometry.addAttribute( 'position', new THREE.BufferAttribute( positions, 3 ) );
  geometry.addAttribute( 'customColor', new THREE.BufferAttribute( colors, 3 ) );
  geometry.addAttribute( 'size', new THREE.BufferAttribute( sizes, 1 ) );

  var material = new THREE.ShaderMaterial( {

    uniforms: {
      color:   { value: new THREE.Color( 0xffffff ) },
      texture: { value: new THREE.TextureLoader().load( "textures/sprites/disc.png" ) }
    },
    vertexShader: document.getElementById( 'vertexshader' ).textContent,
    fragmentShader: document.getElementById( 'fragmentshader' ).textContent,

    alphaTest: 0.9

  } );


  var particles = new THREE.Points( geometry, material );
  return particles;
}

function init() {

  container = document.getElementById( 'container' );

  scene = new THREE.Scene();

  camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
  camera.position.y = 250;
  camera.position.z = 500;

  initGrid(scene);
  particles1 = initParticlesForTemplate('small', 0.01);
  particles2 = initParticlesForTemplate('bus', 0.5);
  scene.add( particles1 );
  scene.add( particles2 );

  renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio( window.devicePixelRatio );
  renderer.setSize( window.innerWidth, window.innerHeight );
  container.appendChild( renderer.domElement );

  controls = new THREE.OrbitControls( camera, renderer.domElement );

  window.addEventListener( 'resize', onWindowResize, false );

}

function onWindowResize() {

  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {

  requestAnimationFrame( animate );

  render();

}

function render() {

  rate = 0.005
  particles1.rotation.y += rate;
  particles2.rotation.y += rate;
  grid.rotation.y += rate;

  renderer.render( scene, camera );

}
