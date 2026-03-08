import React, { useState } from 'react';
import {
  View,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { theme } from '../constants/theme';

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [text, setText] = useState('');

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText('');
  };

  const canSend = text.trim().length > 0 && !disabled;

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
    >
      <View style={styles.container}>
        <TextInput
          style={styles.input}
          placeholder="Message Janus..."
          placeholderTextColor={theme.textMuted}
          value={text}
          onChangeText={setText}
          onSubmitEditing={handleSend}
          editable={!disabled}
          multiline
          maxLength={2000}
        />
        <TouchableOpacity
          style={[styles.button, !canSend && styles.buttonDisabled]}
          onPress={handleSend}
          disabled={!canSend}
          activeOpacity={0.8}
        >
          <SendIcon />
        </TouchableOpacity>
      </View>
      <Text style={styles.disclaimer}>
        Janus may produce inaccurate information about people, places, or facts.
      </Text>
    </KeyboardAvoidingView>
  );
}

function SendIcon() {
  return (
    <View style={styles.iconWrap}>
      <Text style={styles.icon}>➤</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255,255,255,0.05)',
    backgroundColor: 'rgba(30,30,36,0.6)',
  },
  input: {
    flex: 1,
    minHeight: 48,
    maxHeight: 120,
    backgroundColor: 'rgba(18,18,22,0.8)',
    borderRadius: 24,
    paddingHorizontal: 20,
    paddingVertical: 14,
    fontSize: 15,
    color: theme.text,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
  },
  button: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: theme.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  iconWrap: {
    marginLeft: 2,
  },
  icon: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  disclaimer: {
    textAlign: 'center',
    fontSize: 11,
    color: theme.textMuted,
    marginBottom: 8,
  },
});
