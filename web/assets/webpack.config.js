const path = require('path');

var mode = 'production';
var publicPath = '/static/';
if (!process.env.BUILD) {
  mode = 'development';
  publicPath = 'http://localhost:8001' + publicPath
}


module.exports = {
  mode: mode,
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'build/'),
    publicPath: publicPath,
  },
  resolve: {
    extensions: ['.js'],
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: ['style-loader', 'css-loader', 'postcss-loader', 'sass-loader']
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.(jpe?g|png|gif)$/,
        loader: 'file-loader',
        options: {
          name: 'images/[name].[hash].[ext]'
        }
      },
      {
        test: /\.(eot|ttf|ijmap|woff|woff2|svg)$/,
        loader: 'file-loader',
        options: {
          name: 'fonts/[name].[hash].[ext]'
        }
      },
    ],
  },
  devtool: 'eval-source-map',
  devServer: {
    port: 8001
  }
};
