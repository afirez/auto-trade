import * as React from 'react';
import {Button, View, Text} from 'react-native';

// 资产账户结算 只有代理商才显示
export default function AssetsSettlementPage({navigation}) {
  return (
    <View style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
      <Text>AssetsIncomePage</Text>
      <Button title="Go to Home" onPress={() => navigation.navigate('Home')} />
    </View>
  );
}
