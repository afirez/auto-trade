import React, {Component, PropTypes} from 'react';
import {StyleSheet, View, Animated, Dimensions, Text} from 'react-native';
import pxToDp from '../utils/todp';

export const DURATION = {LENGTH_LONG: 2000, LENGTH_SHORT: 2000};
const {height, width} = Dimensions.get('window');
const OPACITY = 0.7;

const dismissKeyboard = require('dismissKeyboard');

export default class ToastUtil extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isShow: false,
      text: '',
      opacityValue: new Animated.Value(OPACITY),
    };
  }
  show(text, duration) {
    if (duration >= DURATION.LENGTH_LONG) {
      this.duration = DURATION.LENGTH_LONG;
    } else {
      this.duration = DURATION.LENGTH_SHORT;
    }
    this.setState({
      isShow: true,
      text: text,
    });
    this.isShow = true;
    this.state.opacityValue.setValue(OPACITY);
    this.close();
  }

  close() {
    if (!this.isShow) return;
    this.timer && clearTimeout(this.timer);
    this.timer = setTimeout(() => {
      Animated.timing(this.state.opacityValue, {
        toValue: 0,
        duration: 1000,
      }).start(() => {
        this.setState({
          isShow: false,
        });
        this.isShow = false;
      });
    }, this.duration);
  }
  componentWillUnmount() {
    this.timer && clearTimeout(this.timer);
  }

  render() {
    let view = this.state.isShow ? (
      <View style={styles.container} pointerEvents="none">
        <Animated.View
          style={[styles.content, {opacity: this.state.opacityValue}]}>
          <Text style={styles.text}>{this.state.text}</Text>
        </Animated.View>
      </View>
    ) : null;
    return view;
  }
}
const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    left: 0,
    top: (height - pxToDp(80)) / 2,
    right: 0,
    alignItems: 'center',
    zIndex: 11,
  },
  content: {
    backgroundColor: '#000',
    opacity: OPACITY,
    borderRadius: pxToDp(12),
    padding: pxToDp(20),
  },
  text: {
    fontSize: pxToDp(28),
    color: '#fff',
  },
});
